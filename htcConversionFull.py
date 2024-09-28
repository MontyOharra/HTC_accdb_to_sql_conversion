from tables.address import createAddressTable, insertAddressData
from utils.sqlHelpers import getSqlServerName
from utils.dbConnections import connectToAccessDatabase, connectToSqlDatabase

def createSqlServerTables(dbConnections):
    
    print('creating tables now')
    createAddressTable(dbConnections)
    print('finished creating tables')
    
def insertDataIntoTables():
    
    insertAddressData()

def main():
    # Check to see if sql Server is set up on the machine
    sqlServerName = getSqlServerName()
    if not sqlServerName:
        return
    
    # Allow user to select whether or not to use the detected sql server name
    '''   
    sqlServerNameIsOk = input(f"SQL Server name is '{sqlServerName}'. Is this ok? [y/n] ")
    if (sqlServerNameIsOk.lower() == 'n'):
        print('[ABORTING CONVERSION PROCESS]')
        return
    '''
    
    htcAllPath = r"C:/HTC_Apps/HTC/HTCAll.accdb"
    sqlDriver = r"ODBC Driver 17 for SQL Server"
    sqlDatabaseName = r"HTC_testing"
    
    print('hello')
    # Default inputs for ease of access
    defaultInputs = input("Do you want to use the default values (HTC Path = rf'C:\HTC_Apps', SQL Driver = 'ODBC Driver 17 for SQL Server', Database Name = 'HTC_Testing'): [y/n] ")
    if (defaultInputs.lower() == "y"):
        htcAllPath = r"C:/HTC_Apps/HTC/HTCAll.accdb"
        sqlDriver = r"ODBC Driver 17 for SQL Server"
        sqlDatabaseName = r"HTC_testing"
    elif (defaultInputs.lower() == "n"):
        htcAllPath = input('Enter the HTC path (Make sure to place a "/" at the end): ')
        sqlDriver = input('Enter the SQL Driver type: ')
        sqlDatabaseName = input('Enter the name of the SQL database to target: ')
      
    
    print('starting connections')
    sqlConn = connectToSqlDatabase(sqlDriver, sqlServerName, sqlDatabaseName)
    print('successful sql')
    htcAllConn = connectToAccessDatabase(htcAllPath)
    print('successful access')
    dbConnections = {
        'sql' : sqlConn,
        'htcAll' : htcAllConn
    }

    createSqlServerTables(dbConnections)
    insertDataIntoTables()
    
if __name__ == "__main__":
    main()