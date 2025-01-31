
from rich.console import Console

from src.utils.helpers import getLogDir, generateAccessDbNameCache
from src.utils.userInput import *
from src.utils.runConversion import runConversion

from .conversionDefinitions.tableConversionDefinitions import *


def main():
    console = Console()
    try:
        logDir = getLogDir()
        connFactories = getDatabaseConnections(
            htcAllPath=r'C:/HTC_Apps/',
            sqlDriver=r'ODBC Driver 17 for SQL Server',
            sqlDatabaseName=r'HTC_Test',
            autoResetDatabase=True
        )
        conversionThreads = getMaxConversionThreads(useMaxConversionThreads=True)
        tablesToMigrate = getTargetTables(forceDefaultPath=True)[0:4]
    except Exception as err:
        console.print(f"[red]{err}[/red]")
        return
    
    accessDbNameCache = generateAccessDbNameCache(tablesToMigrate)
    
    (sqlTableDefinitions, accessConversionDefinitions) = getMigrationDefinitions(conversionThreads, connFactories, tablesToMigrate, accessDbNameCache)
    runConversion(connFactories, conversionThreads, logDir, sqlTableDefinitions, accessConversionDefinitions)
    

if __name__ == "__main__":
    main()


