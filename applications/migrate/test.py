import traceback
from threading import Thread
from queue import Queue
from rich.console import Console

from src.utils.conversionHelpers import convertAccessTables, createSqlTables
from src.utils.richTableOutput import outputSqlCreationLoggingProgress
from src.utils.sqlServerSetup import setupSqlServer

from .definitions import *

def main():
    connFactory, maxConversionThreads = setupSqlServer(
        htcAllPath=r'C:/HTC_Apps/',
        sqlDriver=r'ODBC Driver 17 for SQL Server',
        sqlDatabaseName=r'HTC_Test',
        autoResetDatabase=True,
        useMaxConversionThreads=True
    )
    console = Console()
    
    sqlTableDefinitions, accessConversionDefinitions = getMigrationDefinitions(connFactory)
    
    
    sqlTablesCreationData = {
        tableName : {} for tableName in sqlTableDefinitions.keys()
    }
    # Create SQL tables
    sqlCreationLogQueue = Queue()
    sqlCreationLogThread = Thread(
        target=outputSqlCreationLoggingProgress,
        args=(sqlCreationLogQueue, sqlTablesCreationData, "SQL Server tables creation process has been finished."),
        daemon=True
    )
    sqlCreationLogThread.start()
    
    try:
        createSqlTables(
            connFactory, 
            sqlCreationLogQueue, 
            sqlTableDefinitions,
            maxThreads=maxConversionThreads
        )
        sqlCreationLogQueue.put("COMPLETE")
    except KeyboardInterrupt:
        sqlCreationLogQueue.put("STOP")
    except Exception as e:
        console.print(f"[red]Error creating SQL tables: {e}[/red]")
    finally:
        sqlCreationLogQueue.put("END")
        sqlCreationLogThread.join()
        

    
    accessConversionData = {
        tableName : {} for tableName in accessConversionDefinitions.keys()
    }
    
if __name__ == "__main__":
    main()
