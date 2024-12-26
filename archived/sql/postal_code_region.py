from ...imports import *

postalCodeRegionFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="postal_code_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="region_id", fieldDetails="INTEGER NOT NULL"),
]

postalCodeRegionIndexes: List[Index] = [
]

postalCodeRegionForeignKeys: List[ForeignKey] = [
    ForeignKey('postal_code_region', 'postal_code_id', 'postal_code', 'id'),
    ForeignKey('postal_code_region', 'region_id', 'region', 'id'),
]

def createPostalCodeRegionTable(conn):
    postalCodeRegionTable = SqlTable('postal_code_region', conn, postalCodeRegionFields, postalCodeRegionIndexes, postalCodeRegionForeignKeys)
    postalCodeRegionTable.createTable()
    postalCodeRegionTable.addIndexes()

    return postalCodeRegionTable

def addPostalCodeRegion(
    conn : Connection,
    postalCodeId : int,
    regionId : int,
) -> int:
    data = {
        'postal_code_id' : postalCodeId,
        'region_id' : regionId,
    }
    conn.sqlInsertRow('postal_code_region', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('postal_code_region')