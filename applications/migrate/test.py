from threading import Thread
from queue import Queue
from rich.console import Console

import traceback

from src.utils.conversionHelpers import createSqlTables
from src.utils.richTableOutput import logSqlCreationProgress
from src.utils.sqlServerSetup import setupSqlServer

from .definitions import *

from src.types.types import SqlCreationDetails

def main():
    connFactories, conversionThreads = setupSqlServer(
        htcAllPath=r'C:/HTC_Apps/',
        sqlDriver=r'ODBC Driver 17 for SQL Server',
        sqlDatabaseName=r'HTC_Test',
        autoResetDatabase=True,
        useMaxConversionThreads=True
    )
    sqlConnFactory = connFactories['sql']
    
    sqlTableDefinitions, accessConversionDefinitions = getMigrationDefinitions(connFactories)
    sqlTableCreationData = {
        tableName : SqlCreationDetails("Incomplete", "Incomplete")
         for tableName in sqlTableDefinitions.keys()
    }
    
    console = Console()
    sqlCreationLogQueue = Queue()
    logThread = Thread(
        target=logSqlCreationProgress,
        args=(sqlCreationLogQueue, sqlTableCreationData, "bla bla work done"),
        daemon=False
    )
    logThread.start()
     
    try:
        while True:
            pass
    except KeyboardInterrupt:
        sqlCreationLogQueue.put("STOP")
        logThread.join()
    """
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
"""    
if __name__ == "__main__":
    main()
