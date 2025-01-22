from threading import Thread
from queue import Queue
from rich.console import Console

import traceback

from src.utils.conversionHelpers import createSqlTables
from src.utils.richTableOutput import logSqlCreationProgress
from src.utils.sqlServerSetup import setupSqlServer

from .definitions import *

def main():
    connFactories, conversionThreads = setupSqlServer(
        htcAllPath=r'C:/HTC_Apps/',
        sqlDriver=r'ODBC Driver 17 for SQL Server',
        sqlDatabaseName=r'HTC_Test',
        autoResetDatabase=True,
        useMaxConversionThreads=True
    )
    
    sqlTableDefinitions, accessConversionDefinitions = getMigrationDefinitions(connFactories)
    
    console = Console()
    logQueue = Queue()
    logThread = Thread(
        target=logSqlCreationProgress,
        args=(logQueue, sqlTableDefinitions, "bla bla work done"),
        daemon=True
    )
    logThread.start()
    
    try:
        createSqlTables(
            sqlConnFactory, 
            logQueue, 
            sqlTableDefinitions,
            maxThreads=conversionThreads
        )
        logQueue.put("COMPLETE")
    except KeyboardInterrupt:
        logQueue.put("STOP")
        raise KeyboardInterrupt
    except Exception as e:
        console.print(f"[red]{"Error!"}: {e}\n     {traceback.format_exc()}[/red]")
    finally:
        logQueue.put("END")
        logThread.join()
    
if __name__ == "__main__":
    main()
