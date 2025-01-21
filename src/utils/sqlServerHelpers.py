import pyodbc
import winreg
import socket

from typing import List

from rich.console import Console
from rich.prompt import Prompt, Confirm

from pyodbc import Cursor

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
    
def checkIfDatabaseExists(sqlCursor : Cursor, databaseName : str) -> bool:
    """
        Checks if a database exists on the SQL Server.
        
        sqlCursor - Cursor object for the SQL Server connection.
        databaseName - Name of the database to check.
    """
    checkDbExistsSql = f"SELECT 1 FROM sys.databases WHERE name = {databaseName}"
    sqlCursor.execute(checkDbExistsSql)
    return sqlCursor.fetchone() is not None

def createDatabase(sqlCursor : Cursor, databaseName : str) -> None:
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
    except pyodbc.Error as err:
        console.print(f"[red]Failed to create database '{databaseName}'[/red]")
        exit(1)
        raise err