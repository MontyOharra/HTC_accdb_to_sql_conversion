import traceback
import time
import os

from threading import Thread
from queue import Queue

from src.utils.conversionProcesses import createSqlTables, convertAccessTables
from src.utils.logging import (logSqlCreationProgress, logAccessConversionProgress, logErrors, 
                              readSqlCreationLog, readAccessConversionLog, createLogFile
                              )
from src.utils.helpers import getLogDir, chunkDictionary

from src.classes.AccessConn import AccessConn
from src.classes.SqlServerConn import SqlServerConn


from collections.abc import Callable
from typing import Any
from src.types import SqlCreationDetails, AccessConversionDetails, Field, Index, ForeignKey

def runConversion(
    connFactories : dict[str, Callable[[], AccessConn] | Callable[[], SqlServerConn]], 
    conversionThreads : int,
    sqlTableDefinitions : dict[str, tuple[list[Field], list[Index], list[ForeignKey]]],
    accessConversionDefinitions : dict[str, Callable[[Callable[[], SqlServerConn], list[Any]], None]]
) -> None:
    '''
        connFactories - Dictionary of connection factories for each database. The keys are the database names.
        conversionThreads - Number of threads to use for conversion.
        logDir - Directory to store logs in.
        sqlTableDefinitions - Dictionary of table definitions for each table.
                              Each tuple contains the fields, indexes, and foreign keys for the table.
        accessConversionDefinitions - Dictionary of access conversion functions for each table. The keys are the table names.
                                      Each function takes a connection factory and a list of fields to convert, and returns a list of rows.
    '''

    # Setup logging file
    logDir = getLogDir()
    htcConversionLogPath = os.path.join(logDir, f"htcConversion-{time.time()}.json")  
    # If the log file exists, read the data from it
    # then ask the user if they want to overwrite the 
    # already processes data
    if (os.path.exists(htcConversionLogPath)):
        sqlTableCreationData = readSqlCreationLog(htcConversionLogPath)
        accessTableConversionData = readAccessConversionLog(htcConversionLogPath) 
    # If the log file does not exist, create it and set the data to empty
    else:
        sqlTableCreationLogData = {
            tableName : SqlCreationDetails("Not Started", "Not Started")
            for tableName in sqlTableDefinitions.keys()
        }
        accessTableConversionLogData = {
            tableName : AccessConversionDetails("Not Started", 0, 0, 0)
            for tableName in accessConversionDefinitions.keys()
        }
        createLogFile(htcConversionLogPath)
              
    errorLogQueue = Queue()
    errorLogger = Thread(
        target=logErrors,
        args=(errorLogQueue, htcConversionLogPath),
        daemon=False
    )  
    errorLogger.start()

    chunkSize = 20
    sqlTableCreationLogDataChunked = chunkDictionary(sqlTableCreationLogData, chunkSize)
    sqlTableDefinitionsChunked = chunkDictionary(sqlTableDefinitions, chunkSize)
    tablesCreated = 0
    for idx, _ in enumerate(sqlTableCreationLogDataChunked):
        try:
            sqlCreationLogQueue = Queue()
            sqlCreationProgressLogger = Thread(
                target=logSqlCreationProgress,
                args=(sqlCreationLogQueue, sqlTableCreationLogDataChunked[idx], htcConversionLogPath),
                daemon=False
            )
            sqlCreationProgressLogger.start()
            sqlTablesCreationSucceeded = createSqlTables(
                connFactories['sql'], 
                sqlTableDefinitionsChunked[idx],
                conversionThreads,
                sqlCreationLogQueue, 
                errorLogQueue
            ) 
            if sqlTablesCreationSucceeded:
                tablesCreated += len(sqlTableDefinitionsChunked[idx].keys())
                sqlCreationLogQueue.put(("SUCCESS", f"{tablesCreated} out of {len(sqlTableDefinitions)} SQL tables have been created."))
            else:
                sqlCreationLogQueue.put(("ERROR", "SQL tables creation process has been stopped."))
                errorLogQueue.put(("sqlCreation", "Keyboard interrupt during SQL tables creation process."))
        except Exception as e:
            sqlCreationLogQueue.put(("ERROR", f"Critical Error: {e}\n     {traceback.format_exc()}"))
            errorLogQueue.put(("sqlCreation", f"Critical Error: {e}\n     {traceback.format_exc()}"))
        except KeyboardInterrupt:
            sqlCreationLogQueue.put(("ERROR", f"Keyboard interrupt during SQL tables creation process."))
            errorLogQueue.put(("sqlCreation", "Keyboard interrupt during SQL tables creation process."))
        finally:
            sqlCreationLogQueue.put("STOP")
            sqlCreationProgressLogger.join()
            
    time.sleep(.1)
    chunkSize = 100
    
    accessTableConversionLogDataChunked = chunkDictionary(accessTableConversionLogData, chunkSize)
    accessConversionDefinitionsChunked = chunkDictionary(accessConversionDefinitions, chunkSize)
    tablesConverted = 0
    for idx, _ in enumerate(accessTableConversionLogDataChunked):
        try:
            accessConversionLogQueue = Queue()
            accessConversionProgressLogger = Thread(
                target=logAccessConversionProgress,
                args=(accessConversionLogQueue, accessTableConversionLogDataChunked[idx], htcConversionLogPath),
                daemon=False
            )    
            accessConversionProgressLogger.start()
            accessConversionSucceeded = convertAccessTables(
                    connFactories, 
                    accessConversionDefinitionsChunked[idx],
                    conversionThreads,
                    chunkSize,
                    accessConversionLogQueue, 
                    errorLogQueue
                ) 
            if accessConversionSucceeded:                
                tablesConverted += len(accessConversionDefinitionsChunked[idx].keys())
                accessConversionLogQueue.put(("SUCCESS", f"{tablesConverted} out of {len(accessConversionDefinitions)} Access tables have been converted."))
            else:
                accessConversionLogQueue.put(("ERROR", "Access tables conversion process has been stopped."))
                errorLogQueue.put(("accessConversion", "Keyboard interrupt during Access tables conversion process."))
        except Exception as e:
            accessConversionLogQueue.put(("ERROR", f"Critical Error: {e}\n     {traceback.format_exc()}"))
            errorLogQueue.put(("accessConversion", f"Critical Error: {e}\n     {traceback.format_exc()}"))
        except KeyboardInterrupt:
            accessConversionLogQueue.put(("ERROR", f"Keyboard interrupt during Access tables conversion creation process."))
            errorLogQueue.put(("accessConversion", "Keyboard interrupt during Access tables conversion creation process."))
        finally:
            accessConversionLogQueue.put("STOP")
            errorLogQueue.put("STOP")
            accessConversionProgressLogger.join()
            errorLogger.join()  