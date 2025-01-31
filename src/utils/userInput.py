import os

from .sqlServerSetup import *
from .helpers import getRootDir

from rich.console import Console
from rich.prompt import Prompt, Confirm

from src.classes.ConnFactory import ConnFactory

from collections.abc import Callable

def getDatabaseConnections(
    htcAllPath : str | None = None, 
    sqlDriver : str | None = None, 
    sqlDatabaseName : str | None = None,
    autoResetDatabase : bool = False
) -> dict[str, Callable] :    
    
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
    allSqlServerInstanceNames = getSqlServerInstanceNames()
    if len(allSqlServerInstanceNames) == 0:
        err = "No instances of SQL Server could be found on this machine. Please check SQL Server setup and try again."
        raise Exception(err)
    elif len(allSqlServerInstanceNames) == 1:
        sqlServerName = getSqlServerFullNameFromInstanceName(allSqlServerInstanceNames[0])
    else:
        console.print("[yellow]There are more than one sql servers on this machine. Please choose the server you would like to target:[/yellow]")
        for instanceNumber, instance in enumerate(allSqlServerInstanceNames):
            console.print(f"[blue]{getSqlServerFullNameFromInstanceName(instance)} [{instanceNumber}][/blue]" )
        instanceNum = int(Prompt.ask("[blue]Type the number next to the server instance you would like to select[/blue]"))
        sqlServerName = getSqlServerFullNameFromInstanceName(instance[instanceNum])
    
    # ALlow user input if parameters are not provided
    if htcAllPath == None:
        htcAllPath = Prompt.ask("[blue]Enter the path to the HTC_Apps folder[/blue]")
    if sqlDriver == None:
        useDefaultDriver = Confirm.ask("[blue]Would you like to use the default ODBC driver [ODBC Driver 17 for SQL Server]?[/blue]")
        if useDefaultDriver == False:
            sqlDriver = Prompt.ask("[blue]Enter the name of the driver[/blue]")
        elif useDefaultDriver == True:
            sqlDriver = r'ODBC Driver 17 for SQL Server'
    if sqlDatabaseName == None:
        sqlDatabaseName = Prompt.ask("[blue]Enter the what you want the SQL Server database name to be[/blue]")
    
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
        err = "There was an error establishing a connection to the SQL Server Database."
        raise Exception(err)
      
    initialSqlConn.autocommit = True
    
    # Create database if it does not exist already
    databaseExists = checkIfDatabaseExists(initialSqlConn.cursor(), sqlDatabaseName)
    if not databaseExists:
        try:
            console.print(f"[yellow]The database {sqlDatabaseName} does not exist. Creating it...[/yellow]")
            initialSqlConn.cursor().execute(f"CREATE DATABASE [{sqlDatabaseName}]")
        except pyodbc.Error as err:
            err = "There was an error creating the database."
            raise Exception(err)
        
    # Variable defined here for testing purposes
    # Allow user input in main file
    else:
        resetDatabaseSqlStatement = (
            f"ALTER DATABASE [{sqlDatabaseName}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;"
            f"DROP DATABASE [{sqlDatabaseName}]"
            f"CREATE DATABASE [{sqlDatabaseName}]"
        )
        
        if not autoResetDatabase:
            resetSqlDatabaseAnswer = Confirm.ask("[blue]Would you like to reset the SQL Server database?[/blue]")
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
                err = f"There was an error resetting the database"
                raise Exception(err)

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
        'htc350d': factory.htc350d,
        'htc400Archive': factory.htc400Archive, 
        'htc400': factory.htc400
    }
    
    return conn_factories
  
def getMaxConversionThreads(useMaxConversionThreads : bool = False) -> int:
    cpuCount: int | None = os.cpu_count()
    if cpuCount is None:
        err = "Unable to determine the number of CPUs on this machine. Please check your CPU setup and try again."
        raise Exception(err)
    if not useMaxConversionThreads:
        maxConversionThreads = Prompt.ask("[blue]How many threads would you like to use for conversion? Please enter 'max' to use all avaiable threads[/blue]")
        if maxConversionThreads == 'max':
            maxConversionThreads = 8 or cpuCount - 1
        else:
            maxConversionThreads = int(maxConversionThreads)
    else:
        maxConversionThreads = 8 or cpuCount - 1
        
    return maxConversionThreads
        
def getTargetTables(forceDefaultPath : bool = False) -> list[str]:
    '''
        forceDefaultPath - A boolean value that determines whether the user has
                            input to the target tables text file path. Defaults
                            to false.
        
        Returns a list of strings representing the tables to convert
    '''
    defaultTargetTablesPath = os.path.join(getRootDir(), 'tables.txt')
    
    if forceDefaultPath:
        targetTablesPath = defaultTargetTablesPath
    else:
        if os.path.exists(defaultTargetTablesPath):
            useDefaultTargetTables = Confirm.ask(f"[blue]Found tables.txt file at '{defaultTargetTablesPath}'. Would you like to use this file[/blue]")
            # User selects the default path
            if (useDefaultTargetTables == True):
                targetTablesPath = defaultTargetTablesPath
            # User defines their own path
            elif (useDefaultTargetTables == False):
                targetTablesPath = Prompt.ask("[blue]Please enter the filepath for the tables you could like to convert[/blue]")
        # No default path found, user must supply one
        else:
            targetTablesPath = Prompt.ask("[blue]Could not find tables.txt in directory. Please enter the filepath for the tables you could like to convert[/blue]")
    try:
        with open(targetTablesPath, 'r') as targetTablesFile:
            return [line.strip() for line in targetTablesFile]
    except:
        err = f"Error reading the target table file at '{targetTablesPath}'"
        raise Exception(err)
