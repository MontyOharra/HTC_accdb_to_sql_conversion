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
    createAddressChangeHistoryTable,
    createAgentTable,
    createAgentCertificationTestTable,
    createAgentChangeHistoryTable,
    createArchiveErrorLogTable,
    createArchiveHistoryTable,
    createAssessorialTable,
    createAssessorialChangeHistoryTable,
    createBranchTable,
    createBranchChangeHistoryTable,
    createCertificationTestTable,
    createCertificationTestChangeHistoryTable,
    createCertificationTestTrainerChangeHistoryTable,
    createCertificationTestTrainerTable,
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
      ('HTC000_G010_T010 Company Info', convert_HTC000_G010_T010_Company_Info),
      ('HTC000_G025_T010 Positions', convert_HTC000_G025_T010_Positions),
      ('HTC000_G090_T010 Staff', convert_HTC000_G090_T010_Staff),
      ('HTC010_G000_T000 OrderType Values', convert_HTC010_G000_T000_OrderType_Values),
      # ('HTC010_G000_T000 US Zip Codes', convert_HTC010_G000_T000_US_Zip_Codes),
      ('HTC010_G100_T010 CertificationTestCatalog', convert_HTC010_G100_T010_CertificationTestCatalog),
      ('HTC300_G000_T000 Archive Update History', convert_HTC300_G000_T000_Archive_Update_History),
      ('HTC300_G000_T000 Holidays', convert_HTC300_G000_T000_Holidays),
      ('HTC300_G000_T000 Over Night Update History', convert_HTC300_G000_T000_Over_Night_Update_History),
      ('HTC300_G000_T020 Branch Info', convert_HTC300_G000_T020_Branch_Info),
      ('HTC300_G010_T010 DFW_ACI_Data', convert_HTC300_G010_T010_DFW_ACI_Data),
      ('HTC300_G010_T030 ACI Update History', convert_HTC300_G010_T030_ACI_Update_History),
      ('HTC300_G020_T010 Status Values', convert_HTC300_G020_T010_Status_Values),
      ('HTC300_G020_T030 Status Update History', convert_HTC300_G020_T030_Status_Update_History),
      ('HTC300_G025_T025 Positions Change History', convert_HTC300_G025_T025_Positions_Change_History),
      # ('HTC300_G030_T010 Customers', convert_HTC300_G030_T010_Customers),
      ('HTC300_G030_T030 Customer Update History', convert_HTC300_G030_T030_Customer_Update_History), 
      # ('HTC300_G040_T030 Orders_Update_History', convert_HTC300_G040_T030_Orders_Update_History),
      # ('HTC300_G060_T010 Addresses', convert_HTC300_G060_T010_Addresses),
      # ('HTC300_G060_T030 Addresses_Update_History', convert_HTC300_G060_T030_Addresses_Update_History),
      # ('HTC300_G070_T010 Rates', convert_HTC300_G070_T010_Rates),
      # ('HTC300_G070_T030 Rates_Update_History', convert_HTC300_G070_T030_Rates_Update_History),
      # ('HTC300_G080_T010 Agents', convert_HTC300_G080_T010_Agents),
      # ('HTC300_G080_T020 Agent_Certifications', convert_HTC300_G080_T020_Agent_Certifications),
      # ('HTC300_G080_T030 Agents_Change_History', convert_HTC300_G080_T030_Agents_Change_History),
      # ('HTC300_G090_T030 Staff_Chg_History', convert_HTC300_G090_T030_Staff_Chg_History),
      # ('HTC300_G100_T020 Certification_Trainers', convert_HTC300_G100_T020_Certification_Trainers),
      # ('HTC300_G100_T021 Certifaction_Trainer_Change_History', convert_HTC300_G100_T021_Certifaction_Trainer_Change_History),
      # ('HTC300_G100_T030 CertificationTestCatalogChgHistory', convert_HTC300_G100_T030_CertificationTestCatalogChgHistory),
      # ('HTC400_G900_T010 Archive_Event_Log', convert_HTC400_G900_T010_Archive_Event_Log),
]

sqlTables = []
sqlTables_lock = Lock()


def batch(data, batch_size):
    """Splits data into smaller batches."""
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]


def getRows(connFactory, tableName):
      localConn = connFactory()
      rows = localConn.accessGetTableInfo(tableName[0:6].lower(), tableName)
      localConn.close()
      return rows
    
    
def addToSqlTables(connFactory, createSqlServerTableTask):
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
        for createSqlServerTableTask in createSqlServerTableTasks:
            future = executor.submit(
                addToSqlTables,
                connFactory,
                createSqlServerTableTask
            )
            futures_to_task[future] = createSqlServerTableTask

        for future in as_completed(futures_to_task):
            task = futures_to_task[future]
            try:
                # Add a timeout to detect hanging tasks
                future.result(timeout=30)  # Adjust timeout as needed
            except TimeoutError:
                print(f"Task {task.__name__} timed out.")
            except Exception as e:
                print(f"Task {task.__name__} generated an exception: {e}")

    
def convertAccessTable(connFactory, tableName, rows, rowConversion):
    """
    Converts rows for a specific table in a thread.
    """
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
            try:
                future.result()
            except Exception as e:
                print(f"Task Generated an exception: {e}")


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
    htcAllPath = r'C:/HTC_Apps/'
    sqlDriver = r'ODBC Driver 17 for SQL Server'
    sqlDatabaseName = r'HTC_testing'
    
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
    convertAccessTables(connFactory, maxThreads)
    # addForeignKeysToSqlTables(connFactory, maxThreads)
    
if __name__ == "__main__":
    main()