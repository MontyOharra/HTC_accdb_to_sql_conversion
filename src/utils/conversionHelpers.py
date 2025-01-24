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
    accessDbNameCache['HTC320_ThisCoBr'] = 'htc321'
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
    
    for tableName in sqlTableDefinitions.keys():
        logQueue.put(("SET", tableName))
        
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
                        errorQueue.put(('sqlTableCreation', errorLogMessage))
                except KeyboardInterrupt:
                    for f in futures:
                        f.cancel()
                    raise
                except Exception as err:
                    errorQueue.put(("sqlTableCreation", err))   
            return True
    except KeyboardInterrupt:
        for f in futures:
            f.cancel()
        raise
      
def accessConversionFunction(row, columnNames, accessTableName, sqlConnFactory):
    sqlConn = sqlConnFactory()
    data = {columnNames[i] : row[i] for i in range(len(columnNames))}
    
    for columnName in columnNames:
        if data[columnName] == None:
            rowType = sqlConn.getColumnType(accessTableName, columnName)
            if rowType in ('int', 'float', 'decimal'):
                data[columnName] = 0
            elif rowType in ('nvarchar', 'varchar', 'ntext', 'text'):
                data[columnName] = ''
            # elif rowType == 'datetime2':
            #     dataValue = datetime(1970, 1, 1, 0, 0, 0, 0)
        try:
            data[columnName] = data[columnName].strip().lower()
        except:
            pass
    sqlConn.insertRow(accessTableName, data, allowNulls=False)
    
def convertAccessRows(
    connFactory : Callable,
    tableName : str,
    rowChunk : List[Tuple],
    rowConversion : Callable
) -> Tuple[Tuple[str, AccessConversionDetails], List[Exception]]:
    errorLogMessages = []
    rowsConverted = 0
    rowErrors = 0
    try:
        for row in rowChunk:
            try:
                rowConversion(sqlConnFactory=connFactory, row=row)
                rowsConverted += 1
            except Exception as err:
                rowErrors += 1
                rowsConverted += 1
                errorLogMessages.append(err)
                
        accessConversionDetails = {'rowsConverted' : rowsConverted, 'rowErrors' : rowErrors}   
        accessConversionData = (tableName, accessConversionDetails)          
        return (accessConversionData, errorLogMessages)
    except Exception as err:
        raise
      
def convertAccessTables(    
    connFactories,             # -> returns an AccessConn
    conversionDefinitions: Dict[str, Callable],   # e.g. {tableName: rowConversionFunction, ...}
    maxThreads: int,
    chunkSize : int,
    logQueue: Queue,
    errorQueue: Queue
):
    accessDbNameCache = generateAccessDbNameCache(conversionDefinitions.keys())    
    
    allTasks = []  # each element: (tableName, rowData, rowConversionFunction)
    for tableName, rowConversionFunction in conversionDefinitions.items():
        rows = getRows(connFactories[accessDbNameCache[tableName]], tableName)  # from your existing function
        numRows = len(rows)
        for i in range(0, numRows, chunkSize):
            allTasks.append((tableName, rows[i:i+chunkSize], rowConversionFunction))
        logQueue.put(("SET", (tableName, numRows)))
        
    
    try:
        with ProcessPool(max_workers=maxThreads) as executor:
            futures = [
                executor.schedule(
                    convertAccessRows, args=[
                      connFactories['sql'],
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
                        errorQueue.put(("accessTableConversion", errorLogMessage))
                except KeyboardInterrupt:
                    for f in futures:
                        f.cancel()
                    raise
                except Exception as err:
                    errorQueue.put(("sqlTableCreation", err)) 
            return True
    except KeyboardInterrupt:
        for f in futures:
            f.cancel()
        return False