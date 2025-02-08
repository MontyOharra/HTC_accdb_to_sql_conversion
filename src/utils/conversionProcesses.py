from concurrent.futures import as_completed
from pebble import ProcessPool
from queue import Queue

from src.classes.SqlServerConn import SqlServerConn

from collections.abc import Callable
from typing import Any
from src.types import Field, Index, ForeignKey, SqlCreationDetails

from .helpers import generateAccessDbNameCache

from rich.console import Console

def getRows(
    accessConnFactory : Callable,
    tableName : str
) -> tuple[Any]:
    '''
        accessConnFactory - A function that returns an AccessConn object.
        tableName - Name of the table to get the rows for.
        
        Returns a tuple containing all rows for the table of tableName.
    '''
    conn = accessConnFactory()
    return conn.select(tableName)
  
def createSqlTable(
    sqlConnFactory : Callable[[], SqlServerConn], 
    tableName : str, 
    tableFields : list[Field], 
    tableIndexes : list[Index],
) -> tuple[tuple[str, SqlCreationDetails], list[tuple[str, str, Exception]]]:
    """
        sqlConnFactory - A function that returns a SQL Server connection.
        tableName - Name of the table to create.
        tableFields - List of Field objects representing the fields in the table.
        tableIndexes - List of Index objects representing the indexes on the table.
      
        Create a table in the SQL Server database.
        Send status updates to the sqlCreationLogQueue.
        Send errors to the errorLogQueue.
    """
    # Mark table in progress
    creationStatus = "In Progress"
    indexesStatus = "In Progress"
    errorLogMessages = []
    try:
        sqlConn = sqlConnFactory()
        try:
            # Create table
            sqlConn.createTable(tableName, tableFields)
            creationStatus = "Complete"
        except Exception as err:
            # If there is an error, set creation status to "Failure" and add the error to the error log
            creationStatus = "Failure"
            errorLogMessages.append(("sqlTableCreation", tableName, err))
        try:
            # Add indexes
            for index in tableIndexes:
                sqlConn.addIndex(tableName, index.indexName, index.indexType, index.indexFields, index.isUnique)
            indexesStatus = "Complete"
        except Exception as err:
            # If there is an error, set indexes status to "Failure" and add the error to the error log
            indexesStatus = "Failure"
            errorLogMessages.append(("sqlTableCreation", tableName, err))
            
        # Create a SqlCreationDetails object with the creation and indexes status
        sqlCreationDetails : SqlCreationDetails = SqlCreationDetails(creationStatus, indexesStatus)
        sqlCreationData = (tableName, sqlCreationDetails)
        
        return sqlCreationData, errorLogMessages

    except Exception:
        raise

def createSqlTables(
    sqlConnFactory : Callable, 
    sqlTableDefinitions : dict[str, tuple[list[Field], list[Index], list[ForeignKey]]], 
    maxThreads : int,
    logQueue : Queue,
    errorQueue : Queue
) -> bool: 
    """
        sqlConnFactory - A function that returns a SQL Server connection.
        sqlTableDefinitions - A dictionary of table names and their definitions.
        maxThreads - The maximum number of threads to use for the creation process.
        sqlCreationLogQueue - A queue to send status updates to.
        errorLogQueue - A queue to send errors to.
        
        Uses a multiprocessing pool to create the tables in parallel.
        SQL tables are created in the SQL Server database based on sqlTableDefinitions.
        
        Returns True if the process is complete, False if it is interrupted.
    """
    for tableName in sqlTableDefinitions.keys():
        logQueue.put(("BEGIN", tableName))
        
    try:
        with ProcessPool(max_workers=maxThreads) as executor:
            # Create a list of futures for each table
            # Loops through each table in sqlTableDefinitions
            # Schedules a function to create the table
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
                    # As futures complete, get their creation results
                    sqlCreationData, errorLogMessages = future.result()
                    # Send the creation result to the log queue
                    logQueue.put(('UPDATE', sqlCreationData))
                    for errorLogMessage in errorLogMessages:
                        # Send any errors to the error queue
                        errorQueue.put(('sqlTableCreation', errorLogMessage))
                except KeyboardInterrupt:
                    # Cancel all futures if the process is interrupted
                    for f in futures:
                        f.cancel()
                    raise
                except Exception as err:
                    # If any other error occurs, send it to the error queue
                    errorQueue.put(("sqlTableCreation", err))   
            # Return True to indicate that the process has completed
            return True
    except KeyboardInterrupt:
        # Cancel all futures if the process is interrupted
        # Return False to indicate that the process has been interrupted
        for f in futures:
            f.cancel()
        return False
      
    
def convertAccessRows(
    sqlConnFactory : Callable[[], SqlServerConn],
    tableName : str,
    rowChunk : list[tuple],
    rowConversionFunction : Callable[
                              [Callable[[], SqlServerConn], tuple[Any]], 
                              None
                            ]
) -> tuple[tuple[str, dict[str, int]], list[Exception]]:
    rowsConverted = 0
    rowErrors = 0
    errorLogMessages = []
    try:
        for row in rowChunk:
            try:
                rowConversionFunction(sqlConnFactory, row)
                rowsConverted += 1
            except Exception as err:
                rowErrors += 1
                rowsConverted += 1
                errorLogMessages.append(err)
                
        accessConversionDetails = {'rowsConverted' : rowsConverted, 'rowErrors' : rowErrors}   
        accessConversionData = (tableName, accessConversionDetails)          
        return (accessConversionData, errorLogMessages)
    except KeyboardInterrupt as err:
        raise
      
def convertAccessTables(    
    connFactories,             # -> returns an AccessConn
    conversionDefinitions: dict[str, Callable],   # e.g. {tableName: rowConversionFunction, ...}
    maxThreads: int,
    chunkSize : int,
    logQueue: Queue,
    errorQueue: Queue
):
    accessDbNameCache = generateAccessDbNameCache(list(conversionDefinitions.keys()))     
    console = Console()
    allTasks = []  # each element: (tableName, rowData, rowConversionFunction)
    for tableName, rowConversionFunction in conversionDefinitions.items():
        rows = getRows(connFactories[accessDbNameCache[tableName]], tableName)  # from your existing function
        numRows = len(rows)
        for i in range(0, numRows, chunkSize):
            allTasks.append((tableName, rows[i:i+chunkSize], rowConversionFunction))
        logQueue.put(("BEGIN", (tableName, numRows)))
        
    
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