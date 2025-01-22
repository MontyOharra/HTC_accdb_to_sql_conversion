from concurrent.futures import as_completed
from pebble import ProcessPool
from queue import Queue

from collections.abc import Callable
from typing import Dict, List, Tuple

from src.classes.AccessConn import AccessConn
from src.types.types import Field, Index, ForeignKey, SqlCreationDetails

def generateAccessDbNameCache(tableNames):
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
    sqlCreationLogQueue : Queue, 
    errorLogQueue : Queue
): 
    """
        Create a table in the SQL Server database.
        Send status updates to the sqlCreationLogQueue.
        Send errors to the errorLogQueue.
        
        sqlConnFactory - A function that returns a SQL Server connection.
        tableName - Name of the table to create.
        tableFields - List of Field objects representing the fields in the table.
        tableIndexes - List of Index objects representing the indexes on the table.
        sqlCreationLogQueue - Queue object to send status updates to.
        errorLogQueue - Queue object to send errors to.
    """
    # Mark table in progress
    sqlCreationLogQueue.put((tableName, "creationStatus", "Incomplete"))
    sqlCreationLogQueue.put((tableName, "indexesStatus", "Incomplete"))
    try:
        conn = sqlConnFactory()
        try:
            conn.sqlCreateTable(tableName, tableFields)
            sqlCreationLogQueue.put((tableName, "creationStatus", "Complete"))
        except Exception as err:
            sqlCreationLogQueue.put((tableName, "creationStatus", "Failure"))
            errorLogQueue.put(("sqlTableCreation", tableName, err))

        try:
            for index in tableIndexes:
                conn.sqlAddIndex(tableName, index.indexType, index.indexFields, index.indexName, index.isUnique)
            sqlCreationLogQueue.put((tableName, "indexesStatus", "Complete"))
        except Exception as err:
            sqlCreationLogQueue.put((tableName, "indexesStatus", "Failure"))
            errorLogQueue.put(("sqlTableCreation", tableName, err))

    except KeyboardInterrupt:
        errorLogQueue.put(("sqlTableCreation", tableName, "KeyboardInterrupt"))
        raise

    except Exception as err:
        sqlCreationLogQueue.put((tableName, "creationStatus", "Failure"))
        sqlCreationLogQueue.put((tableName, "indexesStatus", "Failure"))
        errorLogQueue.put(("sqlTableCreation", tableName, err))

def createSqlTables(
    sqlConnFactory : Callable, 
    sqlTableDefinitions : Dict[str, Tuple[List[Field], List[Index], List[ForeignKey]]], 
    maxThreads : int,
    sqlCreationLogQueue : Queue,
    errorLogQueue : Queue
): 
    """
        Create SQL tables in the SQL Server database based on the table definitions.
        
        sqlConnFactory - A function that returns a SQL Server connection.
        sqlTableDefinitions - A dictionary of table names and their definitions.
        maxThreads - The maximum number of threads to use for the creation process.
        sqlCreationLogQueue - A queue to send status updates to.
        errorLogQueue - A queue to send errors to.
    """
    with ProcessPool(maxWorkers=maxThreads) as executor:
        futures = [
            executor.schedule(
                createSqlTable,
                sqlConnFactory,
                tableName,
                fields,
                indexes,
                sqlCreationLogQueue,
                errorLogQueue
            )
            for tableName, (fields, indexes, fks) in sqlTableDefinitions.items()
        ]
        try:
            for future in as_completed(futures):
                try:
                    future.result()
                except KeyboardInterrupt:
                    sqlCreationLogQueue.put("STOP")
                    errorLogQueue.put("STOP")
                    for f in futures:
                        f.cancel()
                    raise
                except Exception as err:
                    errorLogQueue.put(("sqlTableCreation", "UNKNOWN_TABLE", err))
        except KeyboardInterrupt:
            sqlCreationLogQueue.put("STOP")
            errorLogQueue.put("STOP")
            for f in futures:
                f.cancel()
            raise

def convertAccessTable(connFactory, accessConversionLogQueue, tableName, rows, rowConversion): 
    # Mark table in progress
    accessConversionLogQueue.put((tableName, "conversionStatus", "In Progress"))
    
    if not rows:
        accessConversionLogQueue.put((tableName, "totalRows", 0))
        accessConversionLogQueue.put((tableName, "processedRows", 0))
        accessConversionLogQueue.put((tableName, "conversionStatus", "Completed"))
        return
    
    try:
        localConn = connFactory()
        accessConversionLogQueue.put((tableName, "totalRows", len(rows)))
        
        processedRows = 0
        errorCount = 0 
        
        for row in rows:
            try:
                rowConversion(localConn, row)
            except Exception as err:
                errorCount += 1
                # IMPLEMENT LOGGING FUNCTIONALITY
                # print(err)
                accessConversionLogQueue.put((tableName, "errorCount", errorCount))
                continue
            finally:
                processedRows += 1
                accessConversionLogQueue.put((tableName, "processedRows", processedRows))
        
        accessConversionLogQueue.put(tableName, "conversionStatus", "Completed")
            
    except Exception as err:
        accessConversionLogQueue.put((tableName, "conversionStatus", "Failure"))
    finally:
        if localConn:
            localConn.close()

def convertAccessTables(connFactory, accessConversionLogQueue, accessConversionDefinitions, maxThreads = 1): 
    with ThreadPoolExecutor(maxThreads) as executor:
        futures = [
            executor.submit(
                convertAccessTable, 
                connFactory,
                accessConversionLogQueue, 
                tableName,
                getRows(connFactory, tableName),
                rowConversionFunction
            )
            for tableName, rowConversionFunction in accessConversionDefinitions.items()
        ]
        try:
            for future in as_completed(futures):
                future.result()
        except KeyboardInterrupt:
            for f in futures:
                f.cancel()
            raise KeyboardInterrupt
