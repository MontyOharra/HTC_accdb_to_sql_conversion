from ...imports import *

aciDataFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="city_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="postal_code_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="airport_code", fieldDetails="NVARCHAR(5)"),
    Field(fieldName="carrier", fieldDetails="NVARCHAR(50) DEFAULT ''"),
    Field(fieldName="area", fieldDetails="NVARCHAR(1)"),
    Field(fieldName="rate_min", fieldDetails="MONEY"),
    Field(fieldName="rate_100", fieldDetails="MONEY"),
    Field(fieldName="rate_1000", fieldDetails="MONEY"),
    Field(fieldName="rate_2000", fieldDetails="MONEY"),
    Field(fieldName="rate_5000", fieldDetails="MONEY"),
    Field(fieldName="date_created", fieldDetails="DATETIME2"),
    Field(fieldName="created_by", fieldDetails="INTEGER"),
    Field(fieldName="branch_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL DEFAULT (1)"),
]

aciDataIndexes: List[Index] = [
]

aciDataForeignKeys: List[ForeignKey] = [
    ForeignKey('aci_data', 'city_id', 'city', 'id'),
    ForeignKey('aci_data', 'postal_code_id', 'postal_code', 'id'),
    ForeignKey('aci_data', 'created_by', 'user', 'id'),
    ForeignKey('aci_data', 'branch_id', 'branch', 'id'),
]

def createAciDataTable(conn):
    aciDataTable = SqlTable('aci_data', conn, aciDataFields, aciDataIndexes, aciDataForeignKeys)
    aciDataTable.createTable()
    aciDataTable.addIndexes()

    return aciDataTable

def addAciData(
    conn : Connection,
    cityId : int,
    postalCodeId : int,
    airportCode : int,
    carrier : str,
    area : str,
    rateMin : float,
    rate100 : float,
    rate1000 : float,
    rate2000 : float,
    rate5000 : float,
    dateCreated : str,
    createdBy : int,
    branchId : int,
    isActive : bool,
) -> int:
    
    aciDataRow = conn.sqlGetInfo(
        'aci_data',
        'id',
        whereDetails={
            'city_id': cityId,
            'postal_code_id': postalCodeId,
            'airport_code': airportCode,
            'carrier': carrier,
            'area': area,
            'rate_min': rateMin,
            'rate_100': rate100,
            'rate_1000': rate1000,
            'rate_2000': rate2000,
            'rate_5000': rate5000,
            'date_created': dateCreated,
            'created_by': createdBy,
            'branch_id': branchId,
            'is_active': isActive
        }
    )       
    if aciDataRow:
        return aciDataRow[0].id
    data = {
        'city_id' : cityId,
        'postal_code_id' : postalCodeId,
        'airport_code' : airportCode,
        'carrier' : carrier,
        'area' : area,
        'rate_min' : rateMin,
        'rate_100' : rate100,
        'rate_1000' : rate1000,
        'rate_2000' : rate2000,
        'rate_5000' : rate5000,
        'date_created' : dateCreated,
        'created_by' : createdBy,
        'branch_id' : branchId,
        'is_active' : isActive,
    }
    conn.sqlInsertRow('aci_data', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('aci_data')