import traceback
from threading import Thread
from queue import Queue
from rich.console import Console

from src.utils.conversionHelpers import convertAccessTables, createSqlTables
from src.utils.loggingProcesses import outputLoggingTable
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
    sqlTablesCreationData = {
        tableName : {} for tableName in sqlTableDefinitions.keys()
    }
    
    accessConversionData = {
        tableName : {} for tableName in accessConversionDefinitions.keys()
    }

    try:
        # Create SQL tables
        sqlCreationLogQueue = Queue()
        sqlCreationLogThread = Thread(
            target=outputLoggingTable,
            args=(sqlCreationLogQueue, "sqlCreate", sqlTablesCreationData, "SQL Server tables creation process has been finished."),
            daemon=True
        )
        sqlCreationLogThread.start()
        
        accessConversionLogQueue = Queue()
        accessConversionLogThread = Thread(
            target=outputLoggingTable,
            args=(accessConversionLogQueue, "accessConvert", accessConversionData, "Access tables conversion process has been finished."),
            daemon=True
        )
        accessConversionLogThread.start()
        
        try:
            createSqlTables(
                connFactory, 
                sqlCreationLogQueue, 
                sqlTableDefinitions,
                maxThreads=maxConversionThreads
            )
        except Exception as e:
            console.print(f"[red]Error creating SQL tables: {e}[/red]")
        finally:
            sqlCreationLogQueue.put("STOP")
            sqlCreationLogThread.join()
            
        try:          
            convertAccessTables(
                connFactory, 
                accessConversionLogQueue, 
                accessConversionDefinitions, 
                maxThreads=maxConversionThreads
            )
        except Exception as e:
            console.print(f"[red]Error convertion Access tables: {e}[/red]")
        finally:
            accessConversionLogQueue.put("STOP")
            accessConversionLogThread.join()

    except Exception as e:
        console.print(f"[red]Application encountered a critical error: {e} \n Detailed: {traceback.format_exc()}[/red]")

if __name__ == "__main__":
    main()
