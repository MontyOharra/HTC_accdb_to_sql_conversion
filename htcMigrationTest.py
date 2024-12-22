from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import sys
import os
import pyodbc

from src.tables.tableImports import *
from src.imports import *

from src.utils.sqlHelpers import checkIfDatabaseExists, getSqlServerName
from src.utils.dbConnections import getConnection

tablesToConvert = [
    'HTC000_G010_T010 Company Info',
    'HTC000_G025_T010 Positions',
    'HTC000_G090_T010 Staff',
    'HTC010_G000_T000 OrderType Values',
    'HTC010_G000_T000 US Zip Codes',
    'HTC300_G000_T000 Archive Update History',
    'HTC300_G000_T000 Holidays',
    'HTC300_G000_T000 Over Night Update History',
    'HTC300_G000_T020 Branch Info',
    'HTC300_G000_T030 Co Info Chg History',
    'HTC300_G000_T040 Branch Info Chg History',
    'HTC300_G010_T010 DFW_ACI_Data',
    'HTC300_G010_T030 ACI Update History',
    'HTC300_G020_T010 Status Values',
    'HTC300_G020_T030 Status Update History',
    'HTC300_G025_T025 Positions Change History',
    'HTC300_G030_T010 Customers',
    'HTC300_G030_T030 Customer Update History',
    'HTC300_G040_T010A Open Orders',
    'HTC300_G040_T010B Invoiced Orders',
    'HTC300_G040_T010C Remaining Orders',
    'HTC300_G040_T010D Dock Orders',
    'HTC300_G040_T010E Service Orders',
    'HTC400_G040_T010A Orders',    
    'HTC300_G040_T011A Open Order Assessorials',
    'HTC300_G040_T011B Invoiced Order Assessorials',
    'HTC300_G040_T011C Remaining Order Assessorials',
    'HTC300_G040_T011D Dock Order Assessorials',
    'HTC300_G040_T011E Service Order Assessorials',
    'HTC400_G040_T011A Assessorials',
    'HTC300_G040_T012A Open Order Dims',
    'HTC300_G040_T012B Invoiced Order Dims',
    'HTC300_G040_T012C Remaining Order Dims',
    'HTC300_G040_T012D Dock Order Dims',
    'HTC300_G040_T012E Service Order Dims',
    'HTC400_G040_T012A Dims',
    'HTC300_G040_T013A Open Order Drivers',
    'HTC300_G040_T013B Invoiced Order Drivers',
    'HTC300_G040_T013C Remaining Order Drivers',
    'HTC300_G040_T013D Dock Order Drivers',
    'HTC300_G040_T013E Service Order Drivers',
    'HTC400_G040_T013A Drivers',
    'HTC300_G040_T014A Open Order Attachments',
    'HTC300_G040_T014B Invoiced Order Attachments',
    'HTC300_G040_T014C Remaining Order Attachments',
    'HTC300_G040_T014D Dock Order Attachments',
    'HTC300_G040_T014E Service Order Attachments',
    'HTC400_G040_T014A Attachments',
    'HTC300_G040_T030 Orders Update History',
    'HTC300_G050_T010 Accessorials',
    'HTC300_G050_T030 Accessorials Update History',
    'HTC300_G060_T010 Addresses',
    'HTC300_G060_T030 Addresses Update History',
    'HTC300_G070_T010 Rates',
    'HTC300_G070_T030 Rates Update History',
    'HTC300_G080_T010 Agents',
    'HTC300_G090_T030 Staff Chg History',
    'HTC400_G900_T010 Archive Event Log'
]
    
'''    
    'HTC000_G010_T010 Company Info',
    'HTC000_G025_T010 Positions',
    'HTC000_G090_T010 Staff',
    'HTC010_G000_T000 OrderType Values',
    # 'HTC010_G000_T000 US Zip Codes',
    'HTC300_G000_T000 Archive Update History',
    'HTC300_G000_T000 Holidays',
    'HTC300_G000_T000 Over Night Update History',
    'HTC300_G000_T020 Branch Info',
    'HTC300_G000_T030 Co Info Chg History',
    'HTC300_G000_T040 Branch Info Chg History',
    'HTC300_G010_T010 DFW_ACI_Data',
    'HTC300_G010_T030 ACI Update History',
    'HTC300_G020_T010 Status Values',
    # 'HTC300_G020_T030 Status Update History',
    'HTC300_G025_T025 Positions Change History',
    'HTC300_G030_T010 Customers',
    'HTC300_G030_T030 Customer Update History',
    'HTC300_G040_T010A Open Orders',
    'HTC300_G040_T010B Invoiced Orders',
    'HTC300_G040_T010C Remaining Orders',
    # 'HTC300_G040_T010D Dock Orders',
    'HTC300_G040_T010E Service Orders',
    'HTC400_G040_T010A Orders',    
    'HTC300_G040_T011A Open Order Assessorials',
    'HTC300_G040_T011B Invoiced Order Assessorials',
    'HTC300_G040_T011C Remaining Order Assessorials',
    'HTC300_G040_T011D Dock Order Assessorials',
    'HTC300_G040_T011E Service Order Assessorials',
    'HTC400_G040_T011A Assessorials',
    'HTC300_G040_T012A Open Order Dims',
    'HTC300_G040_T012B Invoiced Order Dims',
    'HTC300_G040_T012C Remaining Order Dims',
    'HTC300_G040_T012D Dock Order Dims',
    'HTC300_G040_T012E Service Order Dims',
    'HTC400_G040_T012A Dims',
    'HTC300_G040_T013A Open Order Drivers',
    'HTC300_G040_T013B Invoiced Order Drivers',
    'HTC300_G040_T013C Remaining Order Drivers',
    'HTC300_G040_T013D Dock Order Drivers',
    'HTC300_G040_T013E Service Order Drivers',
    'HTC400_G040_T013A Drivers',
    'HTC300_G040_T014A Open Order Attachments',
    'HTC300_G040_T014B Invoiced Order Attachments',
    'HTC300_G040_T014C Remaining Order Attachments',
    'HTC300_G040_T014D Dock Order Attachments',
    'HTC300_G040_T014E Service Order Attachments',
    'HTC400_G040_T014A Attachments',
    'HTC300_G040_T030 Orders Update History',
    'HTC300_G050_T010 Accessorials',
    'HTC300_G050_T030 Accessorials Update History',
    # 'HTC300_G060_T010 Addresses',
    'HTC300_G060_T030 Addresses Update History',
    'HTC300_G070_T010 Rates',
    'HTC300_G070_T030 Rates Update History',
    'HTC300_G080_T010 Agents',
    'HTC300_G090_T030 Staff Chg History',
    'HTC400_G900_T010 Archive Event Log'
'''  
  
print_lock = Lock()

def safe_print(*args, **kwargs):
    with print_lock:
        print(*args, **kwargs)

def batch(data, batch_size):
    """Splits data into smaller batches."""
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]

def getAccessDbName(tableName):
    if tableName == 'HTC400_G900_T010 Archive Event Log':
        return 'htc400archive'
    else:
        return tableName[0:6].lower()

def getRows(connFactory, tableName):
    localConn = connFactory()
    try:
        rows = localConn.accessGetTableInfo(getAccessDbName(tableName), tableName)
    finally:
        localConn.close()  # Ensure it always closes
    return rows
  
def createSqlServerTable(connFactory, tableName):
    localConn : Connection = connFactory()  # Create a thread-specific connection
    structureDetails = localConn.accessGetTableStructure(getAccessDbName(tableName), tableName)
    fields = []
    for column in structureDetails['columnsInfo']:
        fields.append(Field(column['name'], column['details']))

    localConn.sqlCreateTable(tableName, fields, structureDetails['primaryKeyColumns'])
    sys.stdout.write(f"\rTable [{tableName}] created.\033[K\n")  
    sys.stdout.flush()
    localConn.close()
        
def createSqlServerTables(connFactory, maxThreads):
    with ThreadPoolExecutor(maxThreads) as executor:
        futures = [
            executor.submit(
                createSqlServerTable, 
                connFactory, tableName
            )
            for tableName in tablesToConvert
        ]

        for future in as_completed(futures):
            future.result()
    
def migrateAccessTable(connFactory, tableName, rows):
    localConn = connFactory()
    
    if not rows:
      sys.stdout.write(f"\rThere was no data in [{tableName}]. Completed Conversion.\033[K\n") 
      sys.stdout.flush()
      return
    
    totalRows = len(rows)
    
    columnNames = [column[0] for column in rows[0].cursor_description]
    
    for i, row in enumerate(rows, start=1):
        sys.stdout.write(f"\rMigrating [{tableName}] Table: Current progress is ({round(100*i/totalRows, 1)}%)\033[K") 
        sys.stdout.flush()
        
        data = {}
        for i in range(len(columnNames)):
            if row[i] == None:
                rowType = localConn.sqlGetColumnType(tableName, columnNames[i])
                if rowType in ('int', 'float', 'decimal'):
                    data[columnNames[i]] = 0
                elif rowType in ('nvarchar', 'varchar', 'ntext', 'text'):
                    data[columnNames[i]] = ''
                elif rowType == 'datetime2':
                    data[columnNames[i]] = datetime(1970, 1, 1, 0, 0, 0, 0)
            else:
                data[columnNames[i]] = row[i]
        

        localConn.sqlInsertRow(tableName, data, allowNulls=False)

    sys.stdout.write(f"\rCompleted [{tableName}] Conversion.\033[K\n")
    sys.stdout.flush()
    localConn.close()

def migrateAccessTables(connFactory, maxThreads):
    """
    Distributes the workload across threads and converts data in parallel.
    """

    with ThreadPoolExecutor(maxThreads) as executor:
        futures = [
            executor.submit(
                migrateAccessTable, 
                connFactory, tableName, getRows(connFactory, tableName)
            )
            for tableName in tablesToConvert
        ]

        for future in as_completed(futures):
            future.result()

def main():
    # Variables defined here for testing purposes
    # Allow user input in main file
    htcAllPath = r'C:/HTC_Apps/'
    sqlDriver = r'ODBC Driver 17 for SQL Server'
    sqlDatabaseName = r'HTC_Migration_testing'
    
    sqlServerName = getSqlServerName()
    if not sqlServerName:
        raise ValueError("SQL Server name not found.")
      
    # Setup initial server connection for database creation and reset
    initialSqlServerConnString = (
        f'DRIVER={sqlDriver};'
        f'SERVER={sqlServerName};'
        f'DATABASE=master;'
        'Trusted_Connection=yes;'
    )
    try:
      initialSqlConn = pyodbc.connect(initialSqlServerConnString)
    except pyodbc.Error as e:
        print(f"There was an error connecting to the SQL Server: {e}")
        return
      
    initialSqlConn.autocommit = True
    
    # Create database if it does not exist already
    databaseExists = checkIfDatabaseExists(initialSqlConn.cursor(), sqlDatabaseName)
    if not databaseExists:
        try:
            initialSqlConn.cursor().execute(f"CREATE DATABASE [{sqlDatabaseName}]")
            print(f"The database {sqlDatabaseName} does not exist. Creating it...")
        except pyodbc.Error as e:
            print(f"There was an creating the database: {e}")
            return
        
    # Variable defined here for testing purposes
    # Allow user input in main file
    resetSqlDatabase = True
    if resetSqlDatabase:
      try:
          initialSqlConn.cursor().execute(f"DROP DATABASE [{sqlDatabaseName}]")
          initialSqlConn.cursor().execute(f"CREATE DATABASE [{sqlDatabaseName}]")
          print(f"The database {sqlDatabaseName} exists. Resetting it...")
      except pyodbc.Error as e:
          print(f"There was an error resetting the database: {e}")
          return
        
    # Passdown method to create connections to all HTC databases
    def connFactory():
        return getConnection(
            htcAllPath=htcAllPath,
            sqlDriver=sqlDriver,
            sqlServerName=sqlServerName,
            sqlDatabaseName=sqlDatabaseName
        )
          
    maxThreads = 8
    sys.stdout.write(f"Starting data conversion with {maxThreads} threads...\n")
    
    createSqlServerTables(connFactory, maxThreads)
    migrateAccessTables(connFactory, maxThreads)
    
if __name__ == "__main__":
    main()