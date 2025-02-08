from rich.console import Console

from applications.cli.helpers.userInput import *
from src.utils.runConversion import runConversion
from src.utils.migrationConversionDefinitions.tableConversionDefinitions import getMigrationDefinitions

def main():
    console = Console()
    try:
        connFactories = getDatabaseConnections(
            htcAllPath=r'C:/HTC_Apps/',
            sqlDriver=r'ODBC Driver 17 for SQL Server',
            sqlDatabaseName=r'HTC_Test',
            autoResetDatabase=True
        )
        conversionThreads = getMaxConversionThreads(useMaxConversionThreads=True)
        tablesToMigrate = getTargetTables(forceDefaultPath=True)
    except Exception as err:
        console.print(f"[red]{err}[/red]")
        return
    
    (sqlTableDefinitions, accessConversionDefinitions) = getMigrationDefinitions(conversionThreads, connFactories, tablesToMigrate)
    runConversion(connFactories, conversionThreads, sqlTableDefinitions, accessConversionDefinitions)
    

if __name__ == "__main__":
    main()


