from rich.console import Console
import traceback
from applications.cli.helpers.userInput import *
from src.utils.runConversion import runConversion
from src.utils.migrationConversionDefinitions.tableConversionDefinitions import getMigrationDefinitions
from src.utils.normalizeConversionDefinitions.tableConversionDefinitions import getNormalizationDefinitions

from src.utils.normalizeConversionDefinitions.helpers import countryGet

def main():
    try:
        connFactories = getDatabaseConnections(
            htcAllPath=r'C:/HTC_Apps/',
            sqlDriver=r'ODBC Driver 17 for SQL Server',
            sqlDatabaseName=r'Normalize_Test',
            autoResetDatabase=True
        )
        conversionThreads = getMaxConversionThreads(useMaxConversionThreads=True)
        conversionType = getConversionType()
    except Exception as err:
        raise err

    if conversionType == "migrate":
        tablesToMigrate = getTargetTables()
        (sqlTableDefinitions, accessConversionDefinitions) = getMigrationDefinitions(conversionThreads, connFactories, tablesToMigrate)
        runConversion(connFactories, conversionThreads, sqlTableDefinitions, accessConversionDefinitions)
    elif conversionType == "normalize":
        (sqlTableDefinitions, accessConversionDefinitions) = getNormalizationDefinitions()
        runConversion(connFactories, conversionThreads, sqlTableDefinitions, accessConversionDefinitions)
    

if __name__ == "__main__":
    console = Console()
    from multiprocessing import freeze_support
    freeze_support()    
    
    try:
        main()
    except Exception as err:
        console.print(f"[red]Critical Error: {err}\n     {traceback.format_exc()}")
    finally:
        input("Press Enter to exit...")


