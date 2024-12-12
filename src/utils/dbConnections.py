import pyodbc

from ..imports import Connection


def connectToAccessDatabase(accessDbPath):
    try:
        accessConnStr = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            rf'DBQ={accessDbPath};'
        )
        
        accessConn = pyodbc.connect(accessConnStr)
        return accessConn
    except pyodbc.Error as e:
        print(f"Access Connection Error: {e}")
        raise

def connectToSqlDatabase(sqlDriver, sqlServerName, sqlDatabaseName):
    # Connection to SQL Server database
    try:
        sqlServerConnString = (
            f'DRIVER={sqlDriver};'
            f'SERVER={sqlServerName};'
            f'DATABASE={sqlDatabaseName};'
            'Trusted_Connection=yes;'
        )
        return pyodbc.connect(sqlServerConnString)

    except pyodbc.Error as e:
        print(f"SQL Connection Error: {e}")
        raise
      
def getConnection(htcAllPath, sqlDriver, sqlServerName, sqlDatabaseName):
    try:
        sqlConn = connectToSqlDatabase(sqlDriver, sqlServerName, sqlDatabaseName)

        htc000Conn = connectToAccessDatabase(htcAllPath + 'HTC000_Data_Staff.accdb')
        htc010Conn = connectToAccessDatabase(htcAllPath + 'HTC010_Static_data.accdb')
        htc300Conn = connectToAccessDatabase(htcAllPath + 'HTC300_Data-01-01.accdb')
        htc320Conn = connectToAccessDatabase(htcAllPath + 'HTC320_TSA_Data-01-01.accdb')
        htc350Conn = connectToAccessDatabase(htcAllPath + 'HTC350D ETO Parameters.accdb')
        htc400Conn = connectToAccessDatabase(htcAllPath + 'HTC400_Order Archives.accdb')

        dbConnections = {
            'sqlServer': sqlConn,
            'htc000': htc000Conn,
            'htc010': htc010Conn,
            'htc300': htc300Conn,
            'htc320': htc320Conn,
            'htc350': htc350Conn,
            'htc400': htc400Conn
        }
        return Connection(dbConnections)

    except Exception as e:
        print(f"Error creating connections: {e}")
        raise