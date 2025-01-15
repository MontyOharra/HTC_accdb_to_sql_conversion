import traceback
from threading import Thread
from queue import Queue
from rich.console import Console

from src.utils.conversionHelpers import convertAccessTables, createSqlTables
from src.utils.richTableOutput import outputLoggingTable, outputSqlCreationLoggingProgress, outputAccessConversionLoggingProgress
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
        tableName : {} for tableName in tablesToMigrate
    }
    
    accessConversionData = {
        tableName : {} for tableName in tablesToMigrate
    }
    
    definitionsConn = connFactory()
    
    sqlTableDefinitions = {
        tableName : 
            (
                getSqlTableFields(definitionsConn, tableName), 
                getSqlTableIndexes(definitionsConn, tableName), 
                getSqlTableForeignKeys(definitionsConn, tableName)
            ) for tableName in tablesToMigrate
    }
    
    accessConversionDefinitions = {
        tableName : getAccessConversionFunction(definitionsConn, tableName) for tableName in tablesToMigrate
    }
    
    definitionsConn.close()
    try:
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
        except KeyboardInterrupt:
            console.print("[red]Keyboard interrupt during SQL table creation. Stopping...[/red]")
            # Put STOP on the queue so the logging thread can terminate gracefully
            sqlCreationLogQueue.put("STOP")
            sqlCreationLogThread.join()
            return  # or sys.exit(1)
        except Exception as e:
            console.print(f"[red]Error creating SQL tables: {e}[/red]")
        finally:
            sqlCreationLogQueue.put("STOP")
            sqlCreationLogThread.join()
            print("Hey ginga")
            
        print("this shit working")
            
        try:          
            convertAccessTables(
                connFactory, 
                accessConversionLogQueue, 
                accessConversionDefinitions, 
                maxThreads=maxConversionThreads
            )
            print("this shit aint working")
        except Exception as e:
            console.print(f"[red]Error convertion Access tables: {e}[/red]")
        finally:
            accessConversionLogQueue.put("STOP")
            accessConversionLogThread.join()

    except Exception as e:
        console.print(f"[red]Application encountered a critical error: {e} \n Detailed: {traceback.format_exc()}[/red]")

if __name__ == "__main__":
    main()
