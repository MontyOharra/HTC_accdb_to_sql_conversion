from src.tables.sql.address import createAddressTable

from src.utils.sqlHelpers import getSqlServerName
from src.utils.dbConnections import connectToAccessDatabase, connectToSqlDatabase

from src.imports import *

sqlTables : Dict[str, SqlTable] = {}

def createSqlServerTables(conn : Connection):
    global sqlTables
    
    sqlTables['addressTable'] = createAddressTable(conn)


def addTableForeignKeys(conn : Connection):
    return
    
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
    
    addTableForeignKeys(conn)
    insertDataIntoTables(conn)
    
if __name__ == "__main__":
    main()