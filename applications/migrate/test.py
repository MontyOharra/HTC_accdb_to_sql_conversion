from threading import Thread
from queue import Queue
from rich.console import Console

from src.utils.conversionHelpers import convertAccessTables, createSqlTables
from src.utils.richTableOutput import printSqlCreationProgress, printAccessConversionProgress, processAndOutputData, splitAndProcessOutputData
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
    
    sqlTableDefinitions, accessConversionDefinitions = getMigrationDefinitions(connFactory)
    
    splitAndProcessOutputData(
        connFactory, 
        maxConversionThreads, 
        printSqlCreationProgress, 
        createSqlTables,
        sqlTableDefinitions,
        progressMessage="SQL tables creation current progress:",
        successMessage="All SQL tables have been created.",
        errorMessage="There was an error during the SQL table creation process",
        maxProgressRowCount=10
    )
        
    splitAndProcessOutputData(
        connFactory, 
        maxConversionThreads, 
        printAccessConversionProgress, 
        convertAccessTables,
        accessConversionDefinitions,
        progressMessage="Access conversion progress:",
        successMessage="All access tables have been converted.",
        errorMessage="There was an error during the Access table conversion process",
        maxProgressRowCount=10
    )
    
if __name__ == "__main__":
    main()
