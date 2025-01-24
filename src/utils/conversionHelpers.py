from concurrent.futures import as_completed
from pebble import ProcessPool
from queue import Queue

from collections.abc import Callable
from typing import Dict, List, Tuple

from src.types.types import Field, Index, ForeignKey, SqlCreationDetails, AccessConversionDetails

def generateAccessDbNameCache(tableNames : List[str]) -> Dict[str, str]:
    accessDbNameCache = {
        tableName : tableName[0:6].lower() for tableName in tableNames
    }
    accessDbNameCache['HTC400_G900_T010 Archive Event Log'] = 'htc400archive'
    return accessDbNameCache

def getRows(accessConnFactory : Callable, tableName : str):
    conn = accessConnFactory()
    return conn.select(tableName)

def createSqlTable(
    sqlConnFactory : Callable, 
    tableName : str, 
    tableFields : List[Field], 
    tableIndexes : List[Index],
) -> Tuple[Tuple[str, str, str], List[Tuple[str, str, Exception]]]:
    """
        Create a table in the SQL Server database.
        Send status updates to the sqlCreationLogQueue.
        Send errors to the errorLogQueue.
        
        sqlConnFactory - A function that returns a SQL Server connection.
        tableName - Name of the table to create.
        tableFields - List of Field objects representing the fields in the table.
        tableIndexes - List of Index objects representing the indexes on the table.
    """
    # Mark table in progress
    creationStatus = "In Progress"
    indexesStatus = "In Progress"
    errorLogMessages = []
    try:
        conn = sqlConnFactory()
        try:
            conn.createTable(tableName, tableFields)
            creationStatus = "Complete"
        except Exception as err:
            creationStatus = "Failure"
            errorLogMessages.append(("sqlTableCreation", tableName, err))
        try:
            for index in tableIndexes:
                conn.addIndex(tableName, index.indexType, index.indexFields, index.indexName, index.isUnique)
            indexesStatus = "Complete"
        except Exception as err:
            indexesStatus = "Failure"
            errorLogMessages.append(("sqlTableCreation", tableName, err))
            
        sqlCreationDetails : SqlCreationDetails = SqlCreationDetails(creationStatus, indexesStatus)
        sqlCreationData = (tableName, sqlCreationDetails)
        
        return sqlCreationData, errorLogMessages

    except Exception as err:
        raise

def createSqlTables(
    sqlConnFactory : Callable, 
    sqlTableDefinitions : Dict[str, Tuple[List[Field], List[Index], List[ForeignKey]]], 
    maxThreads : int,
    logQueue : Queue,
    errorQueue : Queue
): 
    """
        Create SQL tables in the SQL Server database based on the table definitions.
        
        sqlConnFactory - A function that returns a SQL Server connection.
        sqlTableDefinitions - A dictionary of table names and their definitions.
        maxThreads - The maximum number of threads to use for the creation process.
        sqlCreationLogQueue - A queue to send status updates to.
        errorLogQueue - A queue to send errors to.
    """
    try:
        with ProcessPool(max_workers=maxThreads) as executor:
            futures = [
                executor.schedule(
                    createSqlTable, args=[
                      sqlConnFactory,
                      tableName,
                      fields,
                      indexes
                    ]
                )
              for tableName, (fields, indexes, fks) in sqlTableDefinitions.items()
            ]
            for future in as_completed(futures):
                try:
                    sqlCreationData, errorLogMessages = future.result()
                    logQueue.put(('UPDATE', sqlCreationData))
                    for errorLogMessage in errorLogMessages:
                        errorQueue.put(errorLogMessage)
                except KeyboardInterrupt:
                    for f in futures:
                        f.cancel()
                    raise
                except Exception as err:
                    errorQueue.put(("sqlTableCreation", "UNKNOWN_TABLE", err))   
            return True
    except KeyboardInterrupt:
        for f in futures:
            f.cancel()
        raise

def convertAccessRows(
    connFactory : Callable,
    tableName : str,
    rowChunk : List[Tuple],
    rowConversion : Callable
) -> Tuple[Tuple[str, AccessConversionDetails], List[Tuple[str, str, Exception]]]:
    errorLogMessages = []
    rowsConverted = 0
    rowErrors = 0
    try:
        conn = connFactory()
        for row in rowChunk:
            try:
                rowConversion(conn, row)
                rowsConverted += 1
            except Exception as err:
                rowErrors += 1
                rowsConverted += 1
                errorLogMessages.append(("accessTableConversion", tableName, err))
                
        accessConversionDetails = {'rowsConverted' : rowsConverted, 'rowErrors' : rowErrors}   
        accessConversionData = (tableName, accessConversionDetails)          
        return (accessConversionData, errorLogMessages)
    except Exception as err:
        raise
      
def convertAccessTables(    
    accessConnFactories,             # -> returns an AccessConn
    conversionDefinitions: Dict[str, Callable],   # e.g. {tableName: rowConversionFunction, ...}
    maxThreads: int,
    chunkSize : int,
    logQueue: Queue,
    errorQueue: Queue
):
    accessDbNameCache = generateAccessDbNameCache(conversionDefinitions.keys())
    conversionStatus = "In Progress"
    totalRows = len(rows)
    
    allTasks = []  # each element: (tableName, rowData, rowConversionFunction)
    for tableName, rowConversionFunction in conversionDefinitions.items():
        print(tableName)
        rows = getRows(accessConnFactories[accessDbNameCache[tableName]], tableName)  # from your existing function
        for i in range(0, len(rows), chunkSize):
            allTasks.append((tableName, rows[i:i+chunkSize], rowConversionFunction))
        logQueue.put(("SET", (tableName, totalRows)))
    
    try:
        with ProcessPool(max_workers=maxThreads) as executor:
            futures = [
                executor.schedule(
                    convertAccessRows, args=[
                      accessConnFactories[accessDbNameCache[tableName]],
                      tableName,
                      rowChunk,
                      rowConversionFunction
                    ]
                )
              for tableName, rowChunk, rowConversionFunction in allTasks
            ]
            for future in as_completed(futures):
                try:
                    accessConversionData, errorLogMessages = future.result()
                    logQueue.put(('UPDATE', accessConversionData))
                    for errorLogMessage in errorLogMessages:
                        errorQueue.put(errorLogMessage)
                except KeyboardInterrupt:
                    raise
                except Exception as err:
                    errorQueue.put(("sqlTableCreation", "UNKNOWN_TABLE", err))   
        return True
    except KeyboardInterrupt:
        for f in futures:
            f.cancel()
        return False