from ...imports import *

phoneFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="country_code", fieldDetails="NVARCHAR(3) NOT NULL"),
    Field(fieldName="area_code", fieldDetails="NVARCHAR(5) NOT NULL"),
    Field(fieldName="phone_number", fieldDetails="NVARCHAR(14) NOT NULL"),
    Field(fieldName="phone_extension", fieldDetails="NVARCHAR(4)"),
]

phoneIndexes: List[Index] = [
]

phoneForeignKeys: List[ForeignKey] = [
]

def createPhoneTable(conn):
    phoneTable = SqlTable('phone', conn, phoneFields, phoneIndexes, phoneForeignKeys)
    phoneTable.createTable()
    phoneTable.addIndexes()

    return phoneTable

def addPhone(
    conn : Connection,
    countryCode : str,
    areaCode : str,
    phoneNumber : str,
    phoneExtension : str,
) -> int:
    if areaCode == '' or phoneNumber == '':
        return 0
    
    phoneRow = conn.sqlGetInfo('phone', 'id',
        whereDetails={
            'country_code' : countryCode,
            'area_code' : areaCode,
            'phone_number' : phoneNumber,
            'phone_extension' : phoneExtension
        }
    )
    if phoneRow:
        return phoneRow[0].id
    data = {
        'country_code' : countryCode,
        'area_code' : areaCode,
        'phone_number' : phoneNumber,
        'phone_extension' : phoneExtension,
    }
    conn.sqlInsertRow('phone', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('phone')