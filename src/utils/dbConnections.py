import pyodbc

from .sqlHelpers import checkIfDatabaseExists

def connectToAccessDatabase(accessDbPath):
    accessConnStr = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        rf'DBQ={accessDbPath};'
    )
    
    accessConn = pyodbc.connect(accessConnStr)
    return accessConn

def connectToSqlDatabase(sqlDriver, sqlServerName, sqlDatabaseName):
    # Connection to SQL Server database
    initialSqlServerConnString = (
        f'DRIVER={sqlDriver};'
        f'SERVER={sqlServerName};'
        f'DATABASE=master;'
        'Trusted_Connection=yes;'
    )
    initialSqlConn = pyodbc.connect(initialSqlServerConnString)
    initialSqlConn.autocommit = True

    databaseExists = checkIfDatabaseExists(initialSqlConn.cursor(), sqlDatabaseName)
    if (not databaseExists):
        createNewDatabase = input(f"The database name {sqlDatabaseName} does not exist within the SQL Server. Would you like to create a database with that name: [y/n]")
        if (createNewDatabase):
          initialSqlConn.cursor().execute(f"CREATE DATABASE [{sqlDatabaseName}]")
        else:
            print('[ABORTING CONVERSION PROCESS]')
            return None

    sqlServerConnString = (
        f'DRIVER={sqlDriver};'
        f'SERVER={sqlServerName};'
        f'DATABASE={sqlDatabaseName};'
        'Trusted_Connection=yes;'
    )

    sqlConn = pyodbc.connect(sqlServerConnString)
    return sqlConn
