from src.tables.sql.country import createCountryTable
from src.tables.sql.address import createAddressTable
from src.tables.sql.postal_code import createPostalCodeTable
from src.tables.sql.city import createCityTable
from src.tables.sql.region import createRegionTable
from src.tables.sql.city_region import createCityRegionTable
from src.tables.sql.city_postal_code import createCityPostalCodeTable
from src.tables.sql.postal_code_region import createPostalCodeRegionTable
from src.tables.sql.company import createCompanyTable
from src.tables.sql.phone import createPhoneTable
from src.tables.sql.fax import createFaxTable
from src.tables.sql.user import createUserTable
from src.tables.sql.position import createPositionTable
from src.tables.sql.order_type import createOrderTypeTable
from src.tables.sql.certification_test import createCertificationTestTable
from src.tables.sql.archive_history import createArchiveHistoryTable
from src.tables.sql.holiday import createHolidayTable
from src.tables.sql.overnight_maintenance_history import createOvernightMaintenanceHistoryTable
from src.tables.sql.branch import createBranchTable
from src.tables.sql.company_change_history import createCompanyChangeHistoryTable
from src.tables.sql.branch_change_history import createBranchChangeHistoryTable
from src.tables.sql.aci_data import createAciDataTable

from src.tables.access.HTC000_G010_T010_Company_Info import convert_HTC000_G010_T010_Company_Info
from src.tables.access.HTC000_G025_T010_Positions import convert_HTC000_G025_T010_Positions
from src.tables.access.HTC000_G090_T010_Staff import convert_HTC000_G090_T010_Staff
from src.tables.access.HTC010_G000_T000_OrderType_Values import convert_HTC010_G000_T000_OrderType_Values
from src.tables.access.HTC010_G000_T000_US_Zip_Codes import convert_HTC010_G000_T000_US_Zip_Codes
from src.tables.access.HTC010_G100_T010_CertificationTestCatalog import convert_HTC010_G100_T010_CertificationTestCatalog
from src.tables.access.HTC300_G000_T000_Archive_Update_History import convert_HTC300_G000_T000_Archive_Update_History
from src.tables.access.HTC300_G000_T000_Holidays import convert_HTC300_G000_T000_Holidays
from src.tables.access.HTC300_G000_T000_Over_Night_Update_History import convert_HTC300_G000_T000_Over_Night_Update_History
from src.tables.access.HTC300_G000_T020_Branch_Info import convert_HTC300_G000_T020_Branch_Info
from src.tables.access.HTC300_G000_T030_Co_Info_Chg_History import convert_HTC300_G000_T030_Co_Info_Chg_History
from src.tables.access.HTC300_G010_T010_DFW_ACI_Data import convert_HTC300_G010_T010_DFW_ACI_Data

from src.utils.sqlHelpers import getSqlServerName
from src.utils.dbConnections import connectToAccessDatabase, connectToSqlDatabase

from src.imports import *

sqlTables : Dict[str, SqlTable] = {}

def createSqlServerTables(conn : Connection):
    global sqlTables
    
    sqlTables['country'] = createCountryTable(conn)
    sqlTables['region'] = createRegionTable(conn)
    sqlTables['address'] = createAddressTable(conn)
    sqlTables['city'] = createCityTable(conn)
    sqlTables['postal_code'] = createPostalCodeTable(conn)
    sqlTables['city_region'] = createCityRegionTable(conn)
    sqlTables['city_postal_code'] = createCityPostalCodeTable(conn)
    sqlTables['postal_code_region'] = createPostalCodeRegionTable(conn)
    sqlTables['company'] = createCompanyTable(conn)
    sqlTables['phone'] = createPhoneTable(conn)
    sqlTables['fax'] = createFaxTable(conn)
    sqlTables['user'] = createUserTable(conn)
    sqlTables['position'] = createPositionTable(conn)
    sqlTables['order_type'] = createOrderTypeTable(conn)
    sqlTables['certification_test'] = createCertificationTestTable(conn)
    sqlTables['archive_history'] = createArchiveHistoryTable(conn)
    sqlTables['holiday'] = createHolidayTable(conn)
    sqlTables['overnight_maintenance_history'] = createOvernightMaintenanceHistoryTable(conn)
    sqlTables['branch'] = createBranchTable(conn)
    sqlTables['company_change_history'] = createCompanyChangeHistoryTable(conn)
    sqlTables['branch_change_history'] = createBranchChangeHistoryTable(conn)
    sqlTables['aci_data'] = createAciDataTable(conn)
    
def addTableForeignKeys(conn : Connection):
    return
    
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
    addTableForeignKeys(conn)
    insertDataIntoTables(conn)

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