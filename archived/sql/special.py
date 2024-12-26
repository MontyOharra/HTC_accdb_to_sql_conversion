from ...imports import *

specialFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="old_id", fieldDetails="INTEGER"),
    Field(fieldName="branch_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="weekday", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="start_time", fieldDetails="TIME NOT NULL"),
    Field(fieldName="end_time", fieldDetails="TIME NOT NULL"),
    Field(fieldName="area", fieldDetails="NVARCHAR(1) NOT NULL"),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL DEFAULT (1)"),
]

specialIndexes: List[Index] = [
]

specialForeignKeys: List[ForeignKey] = [
    ForeignKey('special', 'branch_id', 'branch', 'id'),
]

def createSpecialTable(conn):
    specialTable = SqlTable('special', conn, specialFields, specialIndexes, specialForeignKeys)
    specialTable.createTable()
    specialTable.addIndexes()

    return specialTable

def addSpecial(
    conn : Connection,
    oldId : int,
    branchId : int,
    weekday : int,
    startTime : int,
    endTime : int,
    area : str,
    isActive : bool,
) -> int:
    specialRow = conn.sqlGetInfo(
        'special',
        'id',
        whereDetails={
            'old_id': oldId,
            'branch_id': branchId,
            'weekday': weekday,
            'start_time': startTime,
            'end_time': endTime,
            'area': area,
            'is_active': isActive
        }
    )
    if specialRow:
        return specialRow[0].id

    data = {
        'old_id' : oldId,
        'branch_id' : branchId,
        'weekday' : weekday,
        'start_time' : startTime,
        'end_time' : endTime,
        'area' : area,
        'is_active' : isActive,
    }
    conn.sqlInsertRow('special', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('special')