from ...imports import *

rateAreaFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="rate_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="area", fieldDetails="NVARCHAR(1) NOT NULL"),
    Field(fieldName="rate_min", fieldDetails="MONEY"),
    Field(fieldName="rate_100", fieldDetails="MONEY"),
    Field(fieldName="rate_1000", fieldDetails="MONEY"),
    Field(fieldName="rate_2000", fieldDetails="MONEY"),
    Field(fieldName="rate_5000", fieldDetails="MONEY"),
    Field(fieldName="rate_max", fieldDetails="MONEY"),
]

rateAreaIndexes: List[Index] = [
]

rateAreaForeignKeys: List[ForeignKey] = [
    ForeignKey('rate_area', 'rate_id', 'rate', 'id'),
]

def createRateAreaTable(conn):
    rateAreaTable = SqlTable('rate_area', conn, rateAreaFields, rateAreaIndexes, rateAreaForeignKeys)
    rateAreaTable.createTable()
    rateAreaTable.addIndexes()

    return rateAreaTable

def addRateArea(
    conn : Connection,
    rateId : int,
    area : str,
    rateMin : float,
    rate100 : float,
    rate1000 : float,
    rate2000 : float,
    rate5000 : float,
    rateMax : float,
) -> int:
    rateAreaRow = conn.sqlGetInfo(
        'rate_area',
        'id',
        whereDetails={
            'rate_id': rateId,
            'area': area,
            'rate_min': rateMin,
            'rate_100': rate100,
            'rate_1000': rate1000,
            'rate_2000': rate2000,
            'rate_5000': rate5000,
            'rate_max': rateMax
        }
    )
    if rateAreaRow:
        return rateAreaRow[0].id

    data = {
        'rate_id' : rateId,
        'area' : area,
        'rate_min' : rateMin,
        'rate_100' : rate100,
        'rate_1000' : rate1000,
        'rate_2000' : rate2000,
        'rate_5000' : rate5000,
        'rate_max' : rateMax,
    }
    conn.sqlInsertRow('rate_area', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('rate_area')