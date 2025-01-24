from threading import Thread
from queue import Queue
from rich.console import Console

import traceback
import time
from src.utils.conversionHelpers import createSqlTables, convertAccessTables
from src.utils.loggingProcesses import logSqlCreationProgress, logAccessConversionProgress,logErrors
from src.utils.sqlServerSetup import setupSqlServer

from .definitions import *
from .conversionDefinitions.tablesToMigrate import tablesToMigrateSubset, tablesToMigrateEnd

from src.types.types import SqlCreationDetails, AccessConversionDetails

def main():
    connFactories, conversionThreads = setupSqlServer(
        htcAllPath=r'D:/HTC_Apps/',
        sqlDriver=r'ODBC Driver 17 for SQL Server',
        sqlDatabaseName=r'HTC_Test',
        autoResetDatabase=False,
        useMaxConversionThreads=True
    )
    try:
        console = Console()
        console.print("[yellow]Getting migration definitions...[/yellow]")
        (sqlTableDefinitions, accessConversionDefinitions) = getMigrationDefinitions(conversionThreads, connFactories, tablesToMigrate=tablesToMigrateEnd)
        console.print("[yellow]Beginning migration process[/yellow]")
    except KeyboardInterrupt:
        exit() 
        

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
        errorLogQueue.join()        
if __name__ == "__main__":
    main()
