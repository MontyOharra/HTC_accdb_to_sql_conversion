from ...imports import *

cityPostalCodeFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="city_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="postal_code_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="lat", fieldDetails="DECIMAL NOT NULL"),
    Field(fieldName="lng", fieldDetails="DECIMAL NOT NULL"),
]

cityPostalCodeIndexes: List[Index] = [
]

cityPostalCodeForeignKeys: List[ForeignKey] = [
    ForeignKey('city_postal_code', 'city_id', 'city', 'id'),
    ForeignKey('city_postal_code', 'postal_code_id', 'postal_code', 'id'),
]

def createCityPostalCodeTable(conn):
    cityPostalCodeTable = SqlTable('city_postal_code', conn, cityPostalCodeFields, cityPostalCodeIndexes, cityPostalCodeForeignKeys)
    cityPostalCodeTable.createTable()
    cityPostalCodeTable.addIndexes()

    return cityPostalCodeTable

def addCityPostalCode(
    conn : Connection,
    cityId : int,
    postalCodeId : int,
    lat : float,
    long : float,
) -> int:
    data = {
        'city_id' : cityId,
        'postal_code_id' : postalCodeId,
        'lat' : lat,
        'long' : long,
    }
    conn.sqlInsertRow('city_postal_code', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('city_postal_code')