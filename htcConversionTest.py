from tables.sql.access.address import createAddressTable, insertAddressData, addAddressIndexes
from utils.sqlHelpers import getSqlServerName
from utils.dbConnections import connectToAccessDatabase, connectToSqlDatabase
from utils.connection import Connection

def createSqlServerTables(conn : Connection):
    
    createAddressTable(conn)
    
def addTableIndexes(conn : Connection):
    
    addAddressIndexes(conn)    
    
def addTableForeignKeys(conn : Connection):
    
    pass
    
def insertDataIntoTables(conn : Connection):
    
   pass

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

    conn = Connection(dbConnections)
    
    createSqlServerTables(conn)
    addTableIndexes(conn)
    addTableForeignKeys(conn)
    insertDataIntoTables(conn)
    
if __name__ == "__main__":
    main()