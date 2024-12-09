from ...imports import *

faxFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="country_code", fieldDetails="NVARCHAR(3) NOT NULL"),
    Field(fieldName="area_code", fieldDetails="NVARCHAR(5) NOT NULL"),
    Field(fieldName="fax_number", fieldDetails="NVARCHAR(14) NOT NULL"),
    Field(fieldName="fax_extension", fieldDetails="NVARCHAR(4)"),
]

faxIndexes: List[Index] = [
]

faxForeignKeys: List[ForeignKey] = [
]

def createFaxTable(conn):
    faxTable = SqlTable('fax', conn, faxFields, faxIndexes, faxForeignKeys)
    faxTable.createTable()
    faxTable.addIndexes()

    return faxTable

def addFax(
    conn : Connection,
    countryCode : str,
    areaCode : str,
    faxNumber : str,
    faxExtension : str,
) -> int:        
    faxRow = conn.sqlGetInfo('fax', 'id',
        whereDetails={
            'country_code' : countryCode,
            'area_code' : areaCode,
            'fax_number' : faxNumber,
            'fax_extensino' : faxNumber
        }
    )
    if faxRow:
        return faxRow[0].id
    data = {
        'country_code' : countryCode,
        'area_code' : areaCode,
        'fax_number' : faxNumber,
        'fax_extension' : faxExtension,
    }
    conn.sqlInsertRow('fax', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('fax')