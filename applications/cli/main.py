from rich.console import Console

from applications.cli.helpers.userInput import *
from src.utils.runConversion import runConversion
from src.utils.migrationConversionDefinitions.tableConversionDefinitions import getMigrationDefinitions

def main():
    try:
        connFactories = getDatabaseConnections()
        conversionThreads = getMaxConversionThreads()
        tablesToMigrate = getTargetTables()
    except Exception as err:
        raise err
    
    (sqlTableDefinitions, accessConversionDefinitions) = getMigrationDefinitions(conversionThreads, connFactories, tablesToMigrate)
    runConversion(connFactories, conversionThreads, sqlTableDefinitions, accessConversionDefinitions)
    

if __name__ == "__main__":
    console = Console()
    from multiprocessing import freeze_support
    freeze_support()    
    
    try:
      main()
    except Exception as err:
        console.print(f"[red]Critical Error: {err}")
    finally:
        input("Press Enter to exit...")


