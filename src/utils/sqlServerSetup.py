from src.utils.connectionHelpers import getConnection
from src.utils.sqlServerHelpers import checkIfDatabaseExists, getSqlServerName
import pyodbc

from rich.console import Console
from rich.prompt import Prompt, Confirm
from os import cpu_count

from typing import Tuple
from collections.abc import Callable

def setupSqlServer(
    htcAllPath : str = None, 
    sqlDriver : str = None, 
    sqlDatabaseName : str = None,
    autoResetDatabase : bool = False,
    useMaxConversionThreads : bool = False
) -> Tuple[Callable, int] :    
    
    """ 
        Setup SQL Server connection and create database if it does not exist.
        If parameters are not provided, the user will be prompted to enter them.
        
        htcAllPath - Path to the HTC_Apps folder.
        sqlDriver - Name of the SQL Server driver to use.
        sqlDatabaseName - Name of the SQL Server database to create.
        autoResetDatabase - Reset the SQL Server database if it already exists.
        useMaxConversionThreads - Allows the process to use the maximum number of threads available.
    """
    
    console = Console()
    sqlServerName = getSqlServerName()
    if not sqlServerName:
        raise Exception("SQL Server could not be found on this machine.")
    
    # ALlow user input if parameters are not provided
    if htcAllPath == None:
        htcAllPath = Prompt.ask("Enter the path to the HTC_Apps folder")
    if sqlDriver == None:
        useDefaultDriver = Confirm.ask("Would you like to use the default ODBC driver [ODBC Driver 17 for SQL Server]?")
        if useDefaultDriver == False:
            sqlDriver = Prompt.ask("Enter the name of the driver")
        elif useDefaultDriver == True:
            sqlDriver = r'ODBC Driver 17 for SQL Server'
    if sqlDatabaseName == None:
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
    except pyodbc.Error as err:
        console.print(f"[red]There was an error establishing a connection to the SQL Server Database.[/red]")
        raise err
      
    initialSqlConn.autocommit = True
    
    # Create database if it does not exist already
    databaseExists = checkIfDatabaseExists(initialSqlConn.cursor(), sqlDatabaseName)
    if not databaseExists:
        try:
            console.print(f"[yellow]The database {sqlDatabaseName} does not exist. Creating it...[/yellow]")
            initialSqlConn.cursor().execute(f"CREATE DATABASE [{sqlDatabaseName}]")
        except pyodbc.Error as err:
            console.print(f"[red]There was an error creating the database.[/red]")
            raise err
        
    # Variable defined here for testing purposes
    # Allow user input in main file
    else:
        resetDatabaseSqlStatement = (
            f"ALTER DATABASE [{sqlDatabaseName}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;"
            f"DROP DATABASE [{sqlDatabaseName}]"
            f"CREATE DATABASE [{sqlDatabaseName}]"
        )
        
        if not autoResetDatabase:
            resetSqlDatabaseAnswer = Confirm.ask("Would you like to reset the SQL Server database?")
            if resetSqlDatabaseAnswer == 'y':
                resetDatabase = True
        else:
            resetDatabase = True
        if resetDatabase:
            try:  
                initialSqlConn.cursor().execute(resetDatabaseSqlStatement)
                console.print(f"[yellow]The database {sqlDatabaseName} exists. Resetting it...[/yellow]")
            except pyodbc.Error as err:
                console.print(f"There was an error resetting the database")
                raise err
        
    if not useMaxConversionThreads:
        maxConversionThreads = Prompt.ask("How many threads would you like to use for conversion? Please enter 'max' to use all avaiable threads") 
        if maxConversionThreads == 'max':
            maxConversionThreads = 8 or cpu_count() - 1
        else:
            maxConversionThreads = int(maxConversionThreads)
    else:
        maxConversionThreads = 8 or cpu_count() - 1
        
    console.print(f"[yellow]Using {maxConversionThreads} threads for conversion[/yellow]")
    
    def connFactory() -> pyodbc.Connection:
        return getConnection(
            htcAllPath=htcAllPath,
            sqlDriver=sqlDriver,
            sqlServerName=sqlServerName,
            sqlDatabaseName=sqlDatabaseName
        )
        
    return (connFactory, maxConversionThreads)