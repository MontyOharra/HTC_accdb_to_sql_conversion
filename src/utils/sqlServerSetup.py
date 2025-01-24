import pyodbc
import winreg
import socket
from os import cpu_count

from rich.console import Console
from rich.prompt import Prompt, Confirm

from typing import Dict, List, Tuple
from collections.abc import Callable

from src.classes.SqlServerConn import SqlServerConn
from src.classes.AccessConn import AccessConn
from src.classes.ConnFactory import ConnFactory
    
def createSqlServerConn(sqlDriver, sqlServerName, sqlDatabaseName):
    def getSqlServerConn():
        return SqlServerConn(sqlDriver, sqlServerName, sqlDatabaseName)
    return getSqlServerConn

def createAccessConn(htcAllPath, filename):
    def getAccessConn():
        return AccessConn(htcAllPath, filename)
    return getAccessConn

def getSqlServerInstanceNames() -> List[str]:
    """ 
        Returns a list of local SQL Server instances.
    """
    instances = []

    # Define the registry key path
    keyPath = r"SOFTWARE\Microsoft\Microsoft SQL Server\Instance Names\SQL"
    
    # Open the registry key
    try:
        # Try accessing the 64-bit registry view first
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, keyPath, 0,
                                winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
    except FileNotFoundError:
        # Fall back to the 32-bit registry view
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, keyPath, 0, winreg.KEY_READ)
    
    # Enumerate the instances
    i = 0
    while True:
        try:
            instanceName = winreg.EnumValue(key, i)[0]
            instances.append(instanceName)
            i += 1
        except OSError:
            break  # No more instances
    winreg.CloseKey(key)
        
    return instances

def getSqlServerFullNameFromInstanceName(instanceName: str) -> str:
    """ 
        Returns the full name of a SQL Server instance.
        
        instanceName - Name of the SQL Server instance.
    """
    hostname = socket.gethostname()
    
    if instanceName == "MSSQLSERVER":
        serverName = hostname  # Default instance
    else:
        serverName = f"{hostname}\\{instanceName}"  # Named instance
    
    return serverName

def getFullSqlServerName() -> str:
    """
        Gets the full name of the intended SQL Server instance.
        If there is only one instance, it will be returned.
        If there are multiple instances, the user will be prompted to select one.
    """
    console = Console()
    # Get SQL Server instances
    sqlInstanceNames = getSqlServerInstanceNames()
    if not sqlInstanceNames:
        console.print("There are no sql servers on this machine. Please setup a server and retry the converion. \n [ABORTING CONVERSION PROCCESS]")
        return None
    if len(sqlInstanceNames) == 1: # If there is only one instance, select it
        instance = sqlInstanceNames[0]
        return getSqlServerFullNameFromInstanceName(instance)
    else: # If there are multiple instances, prompt user to select one
        console.print("There are more than one sql servers on this machine. Please choose the server you would like to target:")
        for instanceNumber, instance in enumerate(sqlInstanceNames):
            console.print(f"  {getFullSqlServerName(instance)} [{instanceNumber}]" )
        instanceNum = Prompt.ask("Type the number next to the server instance you would like to select")
        return (getSqlServerFullNameFromInstanceName(instance[instanceNum]))
    
def checkIfDatabaseExists(sqlCursor : pyodbc.Cursor, databaseName : str) -> bool:
    """
        Checks if a database exists on the SQL Server.
        
        sqlCursor - Cursor object for the SQL Server connection.
        databaseName - Name of the database to check.
    """
    console = Console()
    
    checkDbExistsSql = f"SELECT 1 FROM sys.databases WHERE name = '{databaseName}'"
    try:
        sqlCursor.execute(checkDbExistsSql)
        return sqlCursor.fetchone() is not None
    except Exception as err:
        console.print(f"[red]There was an error checking if the database {databaseName} exists.[/red]")
        raise err

def createDatabase(sqlCursor : pyodbc.Cursor, databaseName : str) -> None:
    """
        Creates a database on the SQL Server.
        
        sqlCursor - Cursor object for the SQL Server connection.
        databaseName - Name of the database to create.
    """
    console = Console()
    
    createDbSql = f"CREATE DATABASE [{databaseName}]"
    try:
        sqlCursor.execute(createDbSql)
        console.print(f"Database '{databaseName}' created successfully.")
    except Exception as err:
        console.print(f"[red]Failed to create database '{databaseName}'[/red]")
        exit(1)
        raise err
      
def setupSqlServer(
    htcAllPath : str = None, 
    sqlDriver : str = None, 
    sqlDatabaseName : str = None,
    autoResetDatabase : bool = False,
    useMaxConversionThreads : bool = False
) -> Tuple[Dict[str, Callable], int] :    
    
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
    sqlServerName = getFullSqlServerName()
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
                resetDatabase = False
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

    factory = ConnFactory(sqlDriver, sqlServerName, sqlDatabaseName, htcAllPath)
    
    # Instead of returning a dict of lambdas, return a dict of bound methods
    conn_factories = {
        'sql': factory.sql,              # Note: these are methods on a top-level class
        'htc000': factory.htc000,
        'htc010': factory.htc010,
        'htc300': factory.htc300,
        'htc301': factory.htc301,
        'htc320': factory.htc320,
        'htc321': factory.htc321,
        'htc350': factory.htc350,
        'htc400Archive': factory.htc400Archive, 
        'htc400': factory.htc400
    }
    
    return conn_factories, maxConversionThreads