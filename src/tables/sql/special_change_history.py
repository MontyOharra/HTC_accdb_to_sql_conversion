from ...imports import *

specialChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="special_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="user_id", fieldDetails="INTEGER"),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL"),
]

specialChangeHistoryIndexes: List[Index] = [
]

specialChangeHistoryForeignKeys: List[ForeignKey] = [
    ForeignKey('special_change_history', 'special_id', 'special', 'id'),
    ForeignKey('special_change_history', 'user_id', 'user', 'id'),
]

def createSpecialChangeHistoryTable(conn):
    specialChangeHistoryTable = SqlTable('special_change_history', conn, specialChangeHistoryFields, specialChangeHistoryIndexes, specialChangeHistoryForeignKeys)
    specialChangeHistoryTable.createTable()
    specialChangeHistoryTable.addIndexes()

    return specialChangeHistoryTable

def addSpecialChangeHistory(
    conn : Connection,
    specialId : int,
    userId : int,
    dateChanged : str,
    changes : str,
) -> int:
    specialChangeHistoryRow = conn.sqlGetInfo('special_change_history', 'id', f"[special_id] = '{specialId}' AND [user_id] = '{userId}' AND [date_changed] = '{dateChanged}' AND [changes] = '{changes}'")
    if specialChangeHistoryRow:
        return specialChangeHistoryRow[0].id
    data = {
        'special_id' : specialId,
        'user_id' : userId,
        'date_changed' : dateChanged,
        'changes' : changes,
    }
    conn.sqlInsertRow('special_change_history', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('special_change_history')