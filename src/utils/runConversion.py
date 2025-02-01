import traceback
import time
import os

from threading import Thread
from queue import Queue

from src.utils.conversionProcesses import createSqlTables, convertAccessTables
from src.utils.logging import (logSqlCreationProgress, logAccessConversionProgress, logErrors, 
                              readSqlCreationLog, readAccessConversionLog, 
                              )

from src.types.types import SqlCreationDetails, AccessConversionDetails

def runConversion(connFactories, conversionThreads, logDir, sqlTableDefinitions, accessConversionDefinitions,):
    htcConversionLogPath = os.path.join(logDir, "htcConversion.log")
    if (os.path.exists(htcConversionLogPath)):
        sqlTableCreationData = readSqlCreationLog(htcConversionLogPath)
        pass        
    else:
        sqlTableCreationData = {
            tableName : SqlCreationDetails("Not Started", "Not Started")
            for tableName in sqlTableDefinitions.keys()
        }
    if (False):
        pass
    else:
        accessTableConversionData = {
            tableName : AccessConversionDetails("Not Started", 0, 0, 0)
            for tableName in accessConversionDefinitions.keys()
        }
              
    errorLogQueue = Queue()
    errorLogger = Thread(
        target=logErrors,
        args=(errorLogQueue, logDir),
        daemon=False
    )  
    sqlCreationLogQueue = Queue()
    sqlCreationProgressLogger = Thread(
        target=logSqlCreationProgress,
        args=(sqlCreationLogQueue, sqlTableCreationData, logDir),
        daemon=False
    )
    accessConversionLogQueue = Queue()
    accessConversionProgressLogger = Thread(
        target=logAccessConversionProgress,
        args=(accessConversionLogQueue, accessTableConversionData),
        daemon=False
    )
    '''
    def chunk_dict(d, n):
        items = list(d.items())  # Convert dict items into a list of (key, value) tuples
        return [dict(items[i:i+n]) for i in range(0, len(items), n)]
    
    tablesCreated = 0
    splitsSize = 10
    errorLogger.start()
    for chunk in chunk_dict(sqlTableDefinitions, splitsSize):
        sqlCreationProgressLogger.start()
        if len(chunk) + tablesCreated == len(sqlTableDefinitions):
            successMessage = "SQL tables creation process has been finished."
        else:
            successMessage = f"SQL tables creation progress: {tablesCreated} of {len(sqlTableDefinitions)} tables created."
        try:
            sqlTablesCreationSucceeded = createSqlTables(
                    connFactories['sql'], 
                    chunk,
                    conversionThreads,
                    sqlCreationLogQueue, 
                    errorLogQueue
                ) 
            if sqlTablesCreationSucceeded:
                sqlCreationLogQueue.put(("SUCCESS", successMessage))
            else:
                sqlCreationLogQueue.put(("ERROR", "SQL tables creation process has been stopped."))
                errorLogQueue.put(("sqlCreation", "Keyboard interrupt during SQL tables creation process."))
        except Exception as e:
            sqlCreationLogQueue.put(("ERROR", f"Critical Error: {e}\n     {traceback.format_exc()}"))
            errorLogQueue.put(("sqlCreation", f"Critical Error: {e}\n     {traceback.format_exc()}"))
        except KeyboardInterrupt:
            sqlCreationLogQueue.put(("ERROR", f"Keyboard interrupt during SQL tables creation process."))
            errorLogQueue.put(("sqlCreation", "Keyboard interrupt during SQL tables creation process."))
        sqlCreationProgressLogger.join()
        tablesCreated += len(chunk)
    '''
    
    try:
        sqlCreationProgressLogger.start()
        errorLogger.start()
        sqlTablesCreationSucceeded = createSqlTables(
                    connFactories['sql'], 
                    sqlTableDefinitions,
                    conversionThreads,
                    sqlCreationLogQueue, 
                    errorLogQueue
                ) 
        if sqlTablesCreationSucceeded:
            sqlCreationLogQueue.put(("SUCCESS", "SQL tables creation process has been finished."))
        else:
            sqlCreationLogQueue.put(("ERROR", "SQL tables creation process has been stopped."))
            errorLogQueue.put(("sqlCreation", "Keyboard interrupt during SQL tables creation process."))
    except Exception as e:
        sqlCreationLogQueue.put(("ERROR", f"Critical Error: {e}\n     {traceback.format_exc()}"))
        errorLogQueue.put(("sqlCreation", f"Critical Error: {e}\n     {traceback.format_exc()}"))
    except KeyboardInterrupt:
        sqlCreationLogQueue.put(("ERROR", f"Keyboard interrupt during SQL tables creation process."))
        errorLogQueue.put(("sqlCreation", "Keyboard interrupt during SQL tables creation process."))
        
    time.sleep(1)
    chunkSize = 100
    try:
        accessConversionProgressLogger.start()
        accessConversionSucceeded = convertAccessTables(
                connFactories, 
                accessConversionDefinitions,
                conversionThreads,
                chunkSize,
                accessConversionLogQueue, 
                errorLogQueue
            ) 
        if accessConversionSucceeded:
            accessConversionLogQueue.put(("SUCCESS", f"Access tables conversion process has been finished."))
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
        sqlCreationLogQueue.put("STOP")
        accessConversionProgressLogger.join()
        sqlCreationLogQueue.join()
        errorLogger.join()  