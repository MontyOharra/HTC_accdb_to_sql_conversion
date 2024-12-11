from src.tables.tableImports import *

from src.utils.sqlHelpers import getSqlServerName
from src.utils.dbConnections import connectToAccessDatabase, connectToSqlDatabase

from src.imports import *

sqlTables : List[SqlTable] = []

def createSqlServerTables(conn : Connection):
    global sqlTables
    
    sqlTables.append(createAciDataTable(conn))
    sqlTables.append(createAciDataChangeHistoryTable(conn))
    sqlTables.append(createAddressTable(conn))
    sqlTables.append(createAddressChangeHistoryTable(conn))
    sqlTables.append(createAgentTable(conn))
    sqlTables.append(createAgentCertificationTestTable(conn))
    sqlTables.append(createAgentChangeHistoryTable(conn))
    sqlTables.append(createArchiveErrorLogTable(conn))
    sqlTables.append(createArchiveHistoryTable(conn))
    sqlTables.append(createAssessorialTable(conn))
    sqlTables.append(createAssessorialChangeHistoryTable(conn))
    sqlTables.append(createBranchTable(conn))
    sqlTables.append(createBranchChangeHistoryTable(conn))
    sqlTables.append(createCertificationTestTable(conn))
    sqlTables.append(createCertificationTestChangeHistoryTable(conn))
    sqlTables.append(createCertificationTestTrainerChangeHistoryTable(conn))
    sqlTables.append(createCertificationTestTrainerTable(conn))
    sqlTables.append(createCityPostalCodeTable(conn))
    sqlTables.append(createCityRegionTable(conn))
    sqlTables.append(createCityTable(conn))
    sqlTables.append(createCompanyTable(conn))
    sqlTables.append(createCompanyChangeHistoryTable(conn))
    sqlTables.append(createCountryTable(conn))
    sqlTables.append(createCustomerTable(conn))
    sqlTables.append(createCustomerChangeHistoryTable(conn))
    sqlTables.append(createCustomerDefaultAssessorialTable(conn))
    sqlTables.append(createFaxTable(conn))
    sqlTables.append(createHolidayTable(conn))
    sqlTables.append(createLocationTable(conn))
    sqlTables.append(createLocationChangeHistoryTable(conn))
    sqlTables.append(createLocationDefaultAssessorialTable(conn))
    sqlTables.append(createOrderAssessorialTable(conn))
    sqlTables.append(createOrderAttachmentTable(conn))
    sqlTables.append(createOrderChangeHistoryTable(conn))
    sqlTables.append(createOrderDimTable(conn))
    sqlTables.append(createOrderDriverTable(conn))
    sqlTables.append(createOrderStatusTable(conn))
    sqlTables.append(createOrderStatusChangeHistoryTable(conn))
    sqlTables.append(createOrderTypeTable(conn))
    sqlTables.append(createOrderTable(conn))
    sqlTables.append(createOvernightMaintenanceHistoryTable(conn))
    sqlTables.append(createPhoneTable(conn))
    sqlTables.append(createPositionTable(conn))
    sqlTables.append(createPositionChangeHistoryTable(conn))
    sqlTables.append(createPostalCodeTable(conn))
    sqlTables.append(createPostalCodeRegionTable(conn))
    sqlTables.append(createRateAreaTable(conn))
    sqlTables.append(createRateChangeHistoryTable(conn))
    sqlTables.append(createRateTable(conn))
    sqlTables.append(createRegionTable(conn))
    sqlTables.append(createSpecialChangeHistoryTable(conn))
    sqlTables.append(createSpecialTable(conn))
    sqlTables.append(createUserTable(conn))
    sqlTables.append(createUserChangeHistoryTable(conn))

def addTableForeignKeys(conn : Connection):
    for table in sqlTables:
        table.addForeignKeys()
    
def insertDataIntoTables(conn : Connection):
    convert_HTC000_G010_T010_Company_Info(conn)
    convert_HTC000_G025_T010_Positions(conn)
    convert_HTC000_G090_T010_Staff(conn)
    convert_HTC010_G000_T000_OrderType_Values(conn)
    # convert_HTC010_G000_T000_US_Zip_Codes(conn)
    convert_HTC010_G100_T010_CertificationTestCatalog(conn)
    convert_HTC300_G000_T000_Archive_Update_History(conn)
    convert_HTC300_G000_T000_Holidays(conn)
    convert_HTC300_G000_T000_Over_Night_Update_History(conn)
    convert_HTC300_G000_T020_Branch_Info(conn)
    convert_HTC300_G010_T010_DFW_ACI_Data(conn)
    convert_HTC300_G010_T030_ACI_Update_History(conn)
    convert_HTC300_G020_T010_Status_Values(conn)
    convert_HTC300_G020_T030_Status_Update_History(conn)
    # convert_HTC300_G025_T025_Positions_Change_History(conn)
    # convert_HTC300_G030_T010_Customers(conn)
    # convert_HTC300_G030_T030_Customer_Update_History(conn)
    # convert_HTC300_G040_T030_Orders_Update_History(conn)
    # convert_HTC300_G060_T010_Addresses(conn)
    # convert_HTC300_G060_T030_Addresses_Update_History(conn)
    # convert_HTC300_G070_T010_Rates(conn)
    # convert_HTC300_G070_T030_Rates_Update_History(conn)
    # convert_HTC300_G080_T010_Agents(conn)
    # convert_HTC300_G080_T020_Agent_Certifications(conn)
    # convert_HTC300_G080_T030_Agents_Change_History(conn)
    # convert_HTC300_G090_T030_Staff_Chg_History(conn)
    # convert_HTC300_G100_T020_Certification_Trainers(conn)
    # convert_HTC300_G100_T021_Certifaction_Trainer_Change_History(conn)
    # convert_HTC300_G100_T030_CertificationTestCatalogChgHistory(conn)
    # convert_HTC400_G900_T010_Archive_Event_Log(conn)
   
def main():
    # Check to see if sql Server is set up on the machine
    sqlServerName = getSqlServerName()
    if not sqlServerName:
        return
    
    htcAllPath = r'C:/HTC_Apps/'
    sqlDriver = r'ODBC Driver 17 for SQL Server'
    sqlDatabaseName = r'HTC_testing'
    
    
    sqlConn = connectToSqlDatabase(sqlDriver, sqlServerName, sqlDatabaseName, resetDatabase=True)
    htc000Conn = connectToAccessDatabase(htcAllPath + 'HTC000_Data_Staff.accdb')
    htc010Conn = connectToAccessDatabase(htcAllPath + 'HTC010_Static_data.accdb')
    htc300Conn = connectToAccessDatabase(htcAllPath + 'HTC300_Data-01-01.accdb')
    htc320Conn = connectToAccessDatabase(htcAllPath + 'HTC320_TSA_Data-01-01.accdb')
    htc350Conn = connectToAccessDatabase(htcAllPath + 'HTC350D ETO Parameters.accdb')
    htc400Conn = connectToAccessDatabase(htcAllPath + 'HTC400_Order Archives.accdb')
    dbConnections = {
        'sqlServer' : sqlConn,
        'htc000' : htc000Conn,
        'htc010' : htc010Conn,
        'htc300' : htc300Conn,
        'htc320' : htc320Conn,
        'htc350' : htc350Conn,
        'htc400' : htc400Conn
    }

    conn = Connection(dbConnections)
    
    createSqlServerTables(conn)
    insertDataIntoTables(conn)
    addTableForeignKeys(conn)

def regionGet(**kwargs: str):
    try:
        key: str = next(iter(kwargs))
        return [
            element
            for element in subdivisions_countries.data
            if key in element and kwargs[key].lower() == element[key].lower()
        ]
    except IndexError:
        return {}
    
if __name__ == "__main__":
    main()