from ...imports import *

cityRegionFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="city_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="region_id", fieldDetails="INTEGER NOT NULL"),
]

cityRegionIndexes: List[Index] = [
]

cityRegionForeignKeys: List[ForeignKey] = [
    ForeignKey('city_region', 'city_id', 'city', 'id'),
    ForeignKey('city_region', 'region_id', 'region', 'id'),
]

def createCityRegionTable(conn):
    cityRegionTable = SqlTable('city_region', conn, cityRegionFields, cityRegionIndexes, cityRegionForeignKeys)
    cityRegionTable.createTable()
    cityRegionTable.addIndexes()

    return cityRegionTable

def addCityRegion(
    conn : Connection,
    cityId : int,
    regionId : int,
) -> int:
    data = {
        'city_id' : cityId,
        'region_id' : regionId,
    }
    conn.sqlInsertRow('city_region', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('city_region')