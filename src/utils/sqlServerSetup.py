from src.utils.connectionHelpers import getConnection
from src.utils.sqlServerHelpers import checkIfDatabaseExists, getSqlServerName
import pyodbc

from rich.console import Console
from rich.prompt import Prompt, Confirm
from os import cpu_count

def setupSqlServer(isDefault=True):    
    console = Console()
    sqlServerName = getSqlServerName()
    if not sqlServerName:
        raise Exception("SQL Server could not be found on this machine.")
    
    if isDefault:
        htcAllPath = r'C:/HTC_Apps/'
        sqlDriver = r'ODBC Driver 17 for SQL Server'
        sqlDatabaseName = r'HTC_Test'
    else:
        htcAllPath = Prompt.ask("Enter the path to the HTC_Apps folder")
        useDefaultDriver = Confirm.ask("Would you like to use the default ODBC driver [ODBC Driver 17 for SQL Server]?")
        if useDefaultDriver == False:
            sqlDriver = Prompt.ask("Enter the name of the driver")
        elif useDefaultDriver == True:
            sqlDriver = r'ODBC Driver 17 for SQL Server'
        sqlDatabaseName = Prompt.ask("Enter the what you want the SQL Server database name to be")
      
    # Setup initial server connection for database creation and reset
    initialSqlServerConnString = (
        f'DRIVER={sqlDriver};'
        f'SERVER={sqlServerName};'
        f'DATABASE=master;'
        'Trusted_Connection=yes;'
    )
    try:
        initialSqlConn = pyodbc.connect(initialSqlServerConnString)
    except pyodbc.Error as e:
        raise Exception(f"There was an error connecting to the SQL Server: {e}")
      
    initialSqlConn.autocommit = True
    
    # Create database if it does not exist already
    databaseExists = checkIfDatabaseExists(initialSqlConn.cursor(), sqlDatabaseName)
    if not databaseExists:
        try:
            console.print(f"[yellow]The database {sqlDatabaseName} does not exist. Creating it...[/yellow]")
            initialSqlConn.cursor().execute(f"CREATE DATABASE [{sqlDatabaseName}]")
        except pyodbc.Error as e:
            raise Exception(f"There was an creating the database: {e}")
        
    # Variable defined here for testing purposes
    # Allow user input in main file
    else:
        if isDefault:
            initialSqlConn.cursor().execute(f"DROP DATABASE [{sqlDatabaseName}]")
            initialSqlConn.cursor().execute(f"CREATE DATABASE [{sqlDatabaseName}]")
            console.print(f"[yellow]The database {sqlDatabaseName} exists. Resetting it...[/yellow]")
        else:
            resetSqlDatabase = Confirm.ask("Would you like to reset the SQL Server database? (y/n): ")
            if resetSqlDatabase == 'y':
                try:
                    initialSqlConn.cursor().execute(f"DROP DATABASE [{sqlDatabaseName}]")
                    initialSqlConn.cursor().execute(f"CREATE DATABASE [{sqlDatabaseName}]")
                    print(f"The database {sqlDatabaseName} exists. Resetting it...")
                except pyodbc.Error as e:
                    print(f"There was an error resetting the database: {e}")
                    return
        
  
    if isDefault:
        maxConversionThreads = 8 or cpu_count() - 1
        console.print(f"[yellow]Using {maxConversionThreads} threads for conversion[/yellow]")
    else:
        maxConversionThreads = Prompt.ask("How many threads would you like to use for conversion? Please enter 'max' to use all avaiable threads: ")
        if maxConversionThreads == 'max':
            maxConversionThreads = 8 or cpu_count() - 1
            console.print(f"[yellow]Using {maxConversionThreads} threads for conversion[/yellow]")
        else:
            maxConversionThreads = int(maxConversionThreads)
        
    def connFactory():
        return getConnection(
            htcAllPath=htcAllPath,
            sqlDriver=sqlDriver,
            sqlServerName=sqlServerName,
            sqlDatabaseName=sqlDatabaseName
        )
        
    return (connFactory, maxConversionThreads)