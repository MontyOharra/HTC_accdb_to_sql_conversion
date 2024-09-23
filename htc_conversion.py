import pyodbc

from tables.address import createAddressTable

from utils.getSqlServerName import getUserSqlServerName 

def connectToSqlDatabase(sqlDriver, sqlServerName, sqlDatabaseName):
    # Connection to SQL Server database
    sqlServerConnString = (
        f'DRIVER={sqlDriver};'  # Update driver version if needed
        f'SERVER={sqlServerName};'                 # Replace with your server name
        f'DATABASE={sqlDatabaseName};'             # Replace with your database name
        'Trusted_Connection=yes;'                  # Use 'UID' and 'PWD' for SQL authentication
    )

    sqlConn = pyodbc.connect(sqlServerConnString)
    sqlCursor = sqlConn.cursor()

    return sqlCursor

def createSqlServerTables(sqlDriver, sqlServerName, sqlDatabaseName):
    sqlCursor = connectToSqlDatabase(sqlDriver, sqlServerName, sqlDatabaseName)
    createAddressTable(sqlCursor)

def __main__():
    sqlServerName = getUserSqlServerName()
    print (f'Server Name is: {sqlServerName}')
    if not sqlServerName:
        return
    sqlServerNameIsOk = input(f"SQL Server name is '{sqlServerName}'. Is this ok? [y/n] ")
    if (sqlServerNameIsOk.lower() == 'n'):
        print('[ABORTING CONVERSION PROCESS]')
        return
    
    defaultInputs = input("Do you want to use the default values: [y/n] ")
    if (defaultInputs.lower() == "y"):
        htcPath = r"C:/HTC_Apps/"
        sqlDriver = r"ODBC Driver 17 for SQL Server"
        sqlDatabaseName = r"HTC"
    elif (defaultInputs.lower() == "n"):
        htcPath = input('Enter the HTC path (Make sure to place a "/" at the end): ')
        sqlDriver = input('Enter the SQL Driver type: ')
        sqlDatabaseName = input('Enter the name of the SQL database to target: ')
        
    createSqlServerTables(sqlDriver, sqlServerName, sqlDatabaseName)
    
__main__()