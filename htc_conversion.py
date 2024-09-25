import pyodbc

from tables.address import createAddressTable

from utils.getSqlServerName import getSqlServerName, checkIfDatabaseExists, createDatabase

def connectToSqlDatabase(sqlDriver, sqlServerName, sqlDatabaseName):
    # Connection to SQL Server database
    initialSqlServerConnString = (
        f'DRIVER={sqlDriver};'
        f'SERVER={sqlServerName};'
        f'DATABASE=master;'
        'Trusted_Connection=yes;'
    )
    initialSqlConn = pyodbc.connect(initialSqlServerConnString)

    databaseExists = checkIfDatabaseExists(initialSqlConn, sqlDatabaseName)
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

def createSqlServerTables(sqlConn):
    sqlCursor = sqlConn.cursor()

    createAddressTable(sqlCursor)
    

def __main__():
    
    # Check to see if sql Server is set up on the machine
    sqlServerName = getSqlServerName()
    if not sqlServerName:
        return
    
    # Allow user to select whether or not to use the detected sql server name
    sqlServerNameIsOk = input(f"SQL Server name is '{sqlServerName}'. Is this ok? [y/n] ")
    if (sqlServerNameIsOk.lower() == 'n'):
        print('[ABORTING CONVERSION PROCESS]')
        return
    
    # Default inputs for ease of access
    defaultInputs = input("Do you want to use the default values (HTC Path = 'C:\HTC_Apps', SQL Driver = 'ODBC Driver 17 for SQL Server', Database Name = 'HTC_Testing'): [y/n] ")
    if (defaultInputs.lower() == "y"):
        htcPath = r"C:/HTC_Apps/"
        sqlDriver = r"ODBC Driver 17 for SQL Server"
        sqlDatabaseName = r"HTC_testing"
    elif (defaultInputs.lower() == "n"):
        htcPath = input('Enter the HTC path (Make sure to place a "/" at the end): ')
        sqlDriver = input('Enter the SQL Driver type: ')
        sqlDatabaseName = input('Enter the name of the SQL database to target: ')
      
    
    sqlConn = connectToSqlDatabase(sqlDriver, sqlServerName, sqlDatabaseName)

    createSqlServerTables(sqlConn)
    
__main__()