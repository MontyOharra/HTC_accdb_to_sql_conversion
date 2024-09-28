from tables.address import createAddressTable, insertAddressData
from utils.sqlHelpers import getSqlServerName
from utils.dbConnections import connectToAccessDatabase, connectToSqlDatabase

def createSqlServerTables(dbConnections):
    
    createAddressTable(dbConnections)
    
def insertDataIntoTables():
    
    insertAddressData()

def main():
    # Check to see if sql Server is set up on the machine
    sqlServerName = getSqlServerName()
    if not sqlServerName:
        return
    
    htcAllPath = r"C:/HTC_Apps/HTC/HTC_Backend.accdb"
    sqlDriver = r"ODBC Driver 17 for SQL Server"
    sqlDatabaseName = r"HTC_testing"
    
    
    sqlConn = connectToSqlDatabase(sqlDriver, sqlServerName, sqlDatabaseName)
    htcAllConn = connectToAccessDatabase(htcAllPath)
    dbConnections = {
        'sqlServer' : sqlConn,
        'htcAll' : htcAllConn
    }

    createSqlServerTables(dbConnections)
    insertDataIntoTables()
    
if __name__ == "__main__":
    main()