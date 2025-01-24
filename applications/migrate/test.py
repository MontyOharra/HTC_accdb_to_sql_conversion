from threading import Thread
from queue import Queue
from rich.console import Console

import traceback

from src.utils.conversionHelpers import createSqlTables, convertAccessTables
from src.utils.loggingProcesses import logSqlCreationProgress, logAccessConversionProgress,logErrors
from src.utils.sqlServerSetup import setupSqlServer

from .definitions import *

from .conversionDefinitions.tablesToMigrate import tablesToMigrateSubset

from src.types.types import SqlCreationDetails, AccessConversionDetails

def main():
    connFactories, conversionThreads = setupSqlServer(
        htcAllPath=r'C:/HTC_Apps/',
        sqlDriver=r'ODBC Driver 17 for SQL Server',
        sqlDatabaseName=r'HTC_Test',
        autoResetDatabase=True,
        useMaxConversionThreads=True
    )
    sqlTableDefinitions, accessConversionDefinitions = getMigrationDefinitions(connFactories, tablesToMigrateSubset)
    # ADD CHECKER TO SEE IF LOG FILE EXISTS
    # IF IT DOES, READ IT AND USE IT TO POPULATE THE SQL CREATION DATA
    #     IF THERE ARE CREATED TABLES, ASK USER IF THEY WANT TO OVERWRITE THEM. IF SO, 
    # IF IT DOESN'T, CREATE A NEW LOG FILE AND USE INCOMPLETE FOR THE STATUS
    if (False):
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
        args=(errorLogQueue,),
        daemon=False
    )  
    sqlCreationLogQueue = Queue()
    sqlCreationProgressLogger = Thread(
        target=logSqlCreationProgress,
        args=(sqlCreationLogQueue, sqlTableCreationData),
        daemon=False
    )
    console = Console()
    try:
        errorLogger.start()
        sqlCreationProgressLogger.start()
        sqlTablesCreationSucceeded = createSqlTables(
                connFactories['sql'], 
                sqlTableDefinitions,
                conversionThreads,
                sqlCreationLogQueue, 
                errorLogQueue
            ) 
        if sqlTablesCreationSucceeded:
            sqlCreationLogQueue.put(("SUCCESS", f"SQL tables creation process has been finished."))
        else:
            sqlCreationLogQueue.put(("ERROR", "SQL tables creation process has been stopped."))
            errorLogQueue.put(("sqlCreation", (None, "Keyboard interrupt during SQL tables creation process.")))
    except Exception as e:
        sqlCreationLogQueue.put("ERROR", f"Critical Error: {e}\n     {traceback.format_exc()}")
        errorLogQueue.put(("sqlCreation", (None, f"Critical Error: {e}\n     {traceback.format_exc()}")))
    except KeyboardInterrupt:
        sqlCreationLogQueue.put("ERROR", f"Keyboard interrupt during SQL tables creation process.")
        errorLogQueue.put(("sqlCreation", (None, "Keyboard interrupt during SQL tables creation process.")))
    finally:
        errorLogQueue.put("STOP")
        sqlCreationProgressLogger.join()
        errorLogQueue.join()
    """
    chunkSize = 100
    try:
        errorLogger.start()
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
            errorLogQueue.put(("accessConversion", (None, "Keyboard interrupt during Access tables conversion process.")))
    except Exception as e:
        accessConversionLogQueue.put("ERROR", f"Critical Error: {e}\n     {traceback.format_exc()}")
        errorLogQueue.put(("accessConversion", (None, f"Critical Error: {e}\n     {traceback.format_exc()}")))
    finally:
        accessConversionLogQueue.put("STOP")
        errorLogQueue.put("STOP")
        accessConversionProgressLogger.join()
        errorLogQueue.join()"""
if __name__ == "__main__":
    main()
