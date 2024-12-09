from ...imports import *

positionChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="position_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="user_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL"),
]

positionChangeHistoryIndexes: List[Index] = [
]

positionChangeHistoryForeignKeys: List[ForeignKey] = [
    ForeignKey('position_change_history', 'position_id', 'position', 'id'),
    ForeignKey('position_change_history', 'user_id', 'user', 'id'),
]

def createPositionChangeHistoryTable(conn):
    positionChangeHistoryTable = SqlTable('position_change_history', conn, positionChangeHistoryFields, positionChangeHistoryIndexes, positionChangeHistoryForeignKeys)
    positionChangeHistoryTable.createTable()
    positionChangeHistoryTable.addIndexes()

    return positionChangeHistoryTable

def addPositionChangeHistory(
    conn : Connection,
    positionId : int,
    userId : int,
    dateChanged : str,
    changes : str,
) -> int:
    positionChangeHistoryRow = conn.sqlGetInfo(
    'position_change_history',
    'id',
    whereDetails={
        'position_id': positionId,
        'user_id': userId,
        'date_changed': dateChanged,
        'changes': changes
    }
)
    if positionChangeHistoryRow:
        return positionChangeHistoryRow[0].id
    data = {
        'position_id' : positionId,
        'user_id' : userId,
        'date_changed' : dateChanged,
        'changes' : changes,
    }
    conn.sqlInsertRow('position_change_history', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('position_change_history')