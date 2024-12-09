from ...imports import *

positionFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="position_name", fieldDetails="NVARCHAR(35) NOT NULL"),
    Field(fieldName="security_level", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL"),
    Field(fieldName="branch_id", fieldDetails="INTEGER NOT NULL"),
]

positionIndexes: List[Index] = [
]

positionForeignKeys: List[ForeignKey] = [
    ForeignKey('position', 'branch_id', 'branch', 'id'),
]

def createPositionTable(conn):
    positionTable = SqlTable('position', conn, positionFields, positionIndexes, positionForeignKeys)
    positionTable.createTable()
    positionTable.addIndexes()

    return positionTable

def addPosition(
    conn : Connection,
    positionName : str,
    securityLevel : int,
    isActive : bool,
    branchId : int,
) -> int:
    positionRow = conn.sqlGetInfo(
        'position',
        'id',
        whereDetails={
            'position_name' : positionName,
            'security_level' : securityLevel,
            'is_active' : isActive,
            'branch_id' : branchId
        }
    )
    if positionRow:
        return positionRow[0].id
    data = {
        'position_name' : positionName,
        'security_level' : securityLevel,
        'is_active' : isActive,
        'branch_id' : branchId,
    }
    conn.sqlInsertRow('position', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('position')