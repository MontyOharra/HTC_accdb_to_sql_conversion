import pyodbc
import winreg
import socket

from rich.console import Console
from rich.prompt import Prompt

from typing import Dict, List, Tuple
from collections.abc import Callable

from src.classes.SqlServerConn import SqlServerConn
from src.classes.AccessConn import AccessConn
from src.classes.ConnFactory import ConnFactory
    
def createSqlServerConn(sqlDriver, sqlServerName, sqlDatabaseName) -> SqlServerConn:
    def getSqlServerConn():
        return SqlServerConn(sqlDriver, sqlServerName, sqlDatabaseName)
    return getSqlServerConn

def createAccessConn(htcAllPath, filename) -> AccessConn:
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
        console.print(f"[green]Database: '{databaseName}' created successfully.[/green]")
    except Exception as err:
        console.print(f"[red]Failed to create database: '{databaseName}'.[/red]")
        exit(1)
        raise err
      