from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import sys
import os
import pyodbc

from src.tables.tableImports import *
from src.imports import *

from src.utils.sqlHelpers import checkIfDatabaseExists, getSqlServerName
from src.utils.dbConnections import getConnection

createSqlServerTableTasks = [
    createAciDataTable,
    createAciDataChangeHistoryTable,
    createAddressTable,
    createAgentTable,
    createAgentChangeHistoryTable,
    createArchiveErrorLogTable,
    createArchiveHistoryTable,
    createAssessorialTable,
    createAssessorialChangeHistoryTable,
    createBranchTable,
    createBranchChangeHistoryTable,
    createCityPostalCodeTable,
    createCityRegionTable,
    createCityTable,
    createCompanyTable,
    createCompanyChangeHistoryTable,
    createCountryTable,
    createCustomerTable,
    createCustomerChangeHistoryTable,
    createCustomerDefaultAssessorialTable,
    createFaxTable,
    createHolidayTable,
    createLocationTable,
    createLocationChangeHistoryTable,
    createLocationDefaultAssessorialTable,
    createOrderAssessorialTable,
    createOrderAttachmentTable,
    createOrderChangeHistoryTable,
    createOrderDimTable,
    createOrderDriverTable,
    createOrderStatusTable,
    createOrderStatusChangeHistoryTable,
    createOrderTypeTable,
    createOrderTable,
    createOvernightMaintenanceHistoryTable,
    createPhoneTable,
    createPositionTable,
    createPositionChangeHistoryTable,
    createPostalCodeTable,
    createPostalCodeRegionTable,
    createRateAreaTable,
    createRateChangeHistoryTable,
    createRateTable,
    createRegionTable,
    createSpecialChangeHistoryTable,
    createSpecialTable,
    createUserTable,
    createUserChangeHistoryTable,    
]

tableConversionTasks = [
    #('HTC000_G010_T010 Company Info', convert_HTC000_G010_T010_Company_Info),
    #('HTC000_G025_T010 Positions', convert_HTC000_G025_T010_Positions),
    #('HTC000_G090_T010 Staff', convert_HTC000_G090_T010_Staff),
    #('HTC010_G000_T000 OrderType Values', convert_HTC010_G000_T000_OrderType_Values),
    ## ('HTC010_G000_T000 US Zip Codes', convert_HTC010_G000_T000_US_Zip_Codes),
    #('HTC300_G000_T000 Archive Update History', convert_HTC300_G000_T000_Archive_Update_History),
    #('HTC300_G000_T000 Holidays', convert_HTC300_G000_T000_Holidays),
    #('HTC300_G000_T000 Over Night Update History', convert_HTC300_G000_T000_Over_Night_Update_History),
    #('HTC300_G000_T020 Branch Info', convert_HTC300_G000_T020_Branch_Info),
    #('HTC300_G000_T030 Co Info Chg History', convert_HTC300_G000_T030_Co_Info_Chg_History),
    #('HTC300_G000_T040 Branch Info Chg History', convert_HTC300_G000_T040_Branch_Info_Chg_History),
    #('HTC300_G010_T010 DFW_ACI_Data', convert_HTC300_G010_T010_DFW_ACI_Data),
    #('HTC300_G010_T030 ACI Update History', convert_HTC300_G010_T030_ACI_Update_History),
    #('HTC300_G020_T010 Status Values', convert_HTC300_G020_T010_Status_Values),
    # ## ('HTC300_G020_T030 Status Update History', convert_HTC300_G020_T030_Status_Update_History),
    #('HTC300_G025_T025 Positions Change History', convert_HTC300_G025_T025_Positions_Change_History),
    #('HTC300_G030_T010 Customers', convert_HTC300_G030_T010_Customers),
    #('HTC300_G030_T030 Customer Update History', convert_HTC300_G030_T030_Customer_Update_History),
    #('HTC300_G040_T010A Open Orders', convert_HTC300_G040_T010A_Open_Orders),
    #('HTC300_G040_T010B Invoiced Orders', convert_HTC300_G040_T010B_Invoiced_Orders),
    # ('HTC300_G040_T010C Remaining Orders', convert_HTC300_G040_T010C_Remaining_Orders),
    ## ('HTC300_G040_T010D Dock Orders', convert_HTC300_G040_T010D_Dock_Orders),
    # ('HTC300_G040_T010E Service Orders', convert_HTC300_G040_T010E_Service_Orders),
    # ('HTC400_G040_T010A Orders', convert_HTC400_G040_T010A_Orders),    
    # ('HTC300_G040_T011A Open Order Assessorials', convert_HTC300_G040_T011A_Open_Order_Assessorials),
    # ('HTC300_G040_T011B Invoiced Order Assessorials', convert_HTC300_G040_T011B_Invoiced_Order_Assessorials),
    # ('HTC300_G040_T011C Remaining Order Assessorials', convert_HTC300_G040_T011C_Remaining_Order_Assessorials),
    # ('HTC300_G040_T011D Dock Order Assessorials', convert_HTC300_G040_T011D_Dock_Order_Assessorials),
    # ('HTC300_G040_T011E Service Order Assessorials', convert_HTC300_G040_T011E_Service_Order_Assessorials),
    # ('HTC400_G040_T011A Assessorials', convert_HTC400_G040_T011A_Assessorials),
    # ('HTC300_G040_T012A Open Order Dims', convert_HTC300_G040_T012A_Open_Order_Dims),
    # ('HTC300_G040_T012B Invoiced Order Dims', convert_HTC300_G040_T012B_Invoiced_Order_Dims),
    # ('HTC300_G040_T012C Remaining Order Dims', convert_HTC300_G040_T012C_Remaining_Order_Dims),
    # ('HTC300_G040_T012D Dock Order Dims', convert_HTC300_G040_T012D_Dock_Order_Dims),
    # ('HTC300_G040_T012E Service Order Dims', convert_HTC300_G040_T012E_Service_Order_Dims),
    # ('HTC400_G040_T012A Dims', convert_HTC400_G040_T012A_Dims),
    # ('HTC300_G040_T013A Open Order Drivers', convert_HTC300_G040_T013A_Open_Order_Drivers),
    # ('HTC300_G040_T013B Invoiced Order Drivers', convert_HTC300_G040_T013B_Invoiced_Order_Drivers),
    # ('HTC300_G040_T013C Remaining Order Drivers', convert_HTC300_G040_T013C_Remaining_Order_Drivers),
    # ('HTC300_G040_T013D Dock Order Drivers', convert_HTC300_G040_T013D_Dock_Order_Drivers),
    # ('HTC300_G040_T013E Service Order Drivers', convert_HTC300_G040_T013E_Service_Order_Drivers),
    # ('HTC400_G040_T013A Drivers', convert_HTC400_G040_T013A_Drivers),
    # ('HTC300_G040_T014A Open Order Attachments', convert_HTC300_G040_T014A_Open_Order_Attachments),
    # ('HTC300_G040_T014B Invoiced Order Attachments', convert_HTC300_G040_T014B_Invoiced_Order_Attachments),
    # ('HTC300_G040_T014C Remaining Order Attachments', convert_HTC300_G040_T014C_Remaining_Order_Attachments),
    # ('HTC300_G040_T014D Dock Order Attachments', convert_HTC300_G040_T014D_Dock_Order_Attachments),
    # ('HTC300_G040_T014E Service Order Attachments', convert_HTC300_G040_T014E_Service_Order_Attachments),
    # ('HTC400_G040_T014A Attachments', convert_HTC400_G040_T014A_Attachments),
    # ('HTC300_G040_T030 Orders Update History', convert_HTC300_G040_T030_Orders_Update_History),
    # ('HTC300_G050_T010 Accessorials', convert_HTC300_G050_T010_Accessorials),
    ('HTC300_G050_T030 Accessorials Update History', convert_HTC300_G050_T030_Accessorials_Update_History),
    # ('HTC300_G060_T010 Addresses', convert_HTC300_G060_T010_Addresses),
    # ('HTC300_G060_T030 Addresses Update History', convert_HTC300_G060_T030_Addresses_Update_History),
]
'''    
    ('HTC300_G070_T010 Rates', convert_HTC300_G070_T010_Rates),
    ('HTC300_G070_T030 Rates Update History', convert_HTC300_G070_T030_Rates_Update_History),
    ('HTC300_G080_T010 Agents', convert_HTC300_G080_T010_Agents),
    ('HTC300_G090_T030 Staff Chg History', convert_HTC300_G090_T030_Staff_Chg_History),
    ('HTC400_G900_T010 Archive Event Log', convert_HTC400_G900_T010_Archive_Event_Log),'''


sqlTables = []
sqlTables_lock = Lock()


def batch(data, batch_size):
    """Splits data into smaller batches."""
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]


def getRows(connFactory, tableName):
      localConn = connFactory()
      if tableName == 'HTC400_G900_T010 Archive Event Log':
          rows = localConn.accessGetTableInfo('htc400archive', tableName)
      else:
          rows = localConn.accessGetTableInfo(tableName[0:6].lower(), tableName)
      localConn.close()
      return rows
    
    
def createSqlServerTable(connFactory, createSqlServerTableTask):
    global sqlTables
    try:
        localConn = connFactory()
        result = createSqlServerTableTask(localConn)
        with sqlTables_lock:
            sqlTables.append(result)
        localConn.close()
    except Exception as e:
        print(f"Error in task {createSqlServerTableTask.__name__}: {e}")
        
def createSqlServerTables(connFactory, maxThreads):
    futures_to_task = {}
    with ThreadPoolExecutor(maxThreads) as executor:
        futures = [
            executor.submit(
                createSqlServerTable, 
                connFactory, createSqlServerTableTask
            )
            for createSqlServerTableTask in createSqlServerTableTasks
        ]

        for future in as_completed(futures):
            future.result()

    
def convertAccessTable(connFactory, tableName, rows, rowConversion):
    """
    Converts rows for a specific table in a thread.
    """
    if not rows:
      sys.stdout.write(f"\rThere was no data in [{tableName}]. Completed Conversion.\033[K\n") 
      sys.stdout.flush()
    
    localConn = connFactory()  # Create a thread-specific connection
    totalRows = len(rows)
    for i, row in enumerate(rows, start=1):
        sys.stdout.write(f"\rConverting [{tableName}] Table: Current progress is ({round(100*i/totalRows, 1)}%)\033[K") 
        sys.stdout.flush()

        # Process the row (placeholder logic)
        rowConversion(localConn, row)  # Replace with your row-processing logic

    sys.stdout.write(f"\rCompleted [{tableName}] Conversion.\033[K\n")
    sys.stdout.flush()
    localConn.close()

def convertAccessTables(connFactory, maxThreads, batchSize=100):
    """
    Distributes the workload across threads and converts data in parallel.
    """

    with ThreadPoolExecutor(maxThreads) as executor:
        futures = [
            executor.submit(
                convertAccessTable, 
                connFactory, tableName, getRows(connFactory, tableName), tableConversionDefinition
            )
            for tableName, tableConversionDefinition in tableConversionTasks
        ]

        for future in as_completed(futures):
            future.result()


def addForeignKeysToSqlTable(connFactory, sqlTable : SqlTable):
    localConn = connFactory()
    sqlTable.openNewConnection(localConn)
    sqlTable.addForeignKeys()
    localConn.close()

def addForeignKeysToSqlTables(connFactory, maxThreads):
    with ThreadPoolExecutor(maxThreads) as executor:
        futures = [
            executor.submit(
                addForeignKeysToSqlTable,
                connFactory,
                sqlTable
            )
            for sqlTable in sqlTables
        ]
        
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Task Generated an exception: {e}")

def main():
    # Variables defined here for testing purposes
    # Allow user input in main file
    
    htcAllPath = str(input("Enter the path to the HTC_Apps folder: "))
    useDifferentDriver = str(input("Default is ODBC Driver 17 for SQL Server. Would you like to enter a different driver name? (y/n): "))
    if useDifferentDriver == 'y':
        sqlDriver = str(input("Enter the name of the driver: "))
    elif useDifferentDriver == 'n':
        sqlDriver = r'ODBC Driver 17 for SQL Server'
    sqlDatabaseName = str(input("Enter the what you want the SQL Server database name to be: "))
    
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
    else:
      resetSqlDatabase = str(input("Would you like to reset the SQL Server database? (y/n): "))
      if resetSqlDatabase == 'y':
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
      
    maxThreads = str(input("How many threads would you like to use for the conversion? Please enter 'max' to use all avaiable threads: "))
    if maxThreads == 'max':
        maxThreads = 8 or os.cpu_count()
    else:
        maxThreads = int(maxThreads)
    sys.stdout.write(f"Starting data conversion with {maxThreads} threads...\n")
    
    createSqlServerTables(connFactory, maxThreads)
    convertAccessTables(connFactory, maxThreads)
    # addForeignKeysToSqlTables(connFactory, maxThreads)
    
if __name__ == "__main__":
    main()