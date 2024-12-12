from ...imports import *

assessorialChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="assessorial_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="user_id", fieldDetails="INTEGER"),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL"),
]

assessorialChangeHistoryIndexes: List[Index] = [
]

assessorialChangeHistoryForeignKeys: List[ForeignKey] = [
    ForeignKey('assessorial_change_history', 'assessorial_id', 'assessorial', 'id'),
    ForeignKey('assessorial_change_history', 'user_id', 'user', 'id'),
]

def createAssessorialChangeHistoryTable(conn):
    assessorialChangeHistoryTable = SqlTable('assessorial_change_history', conn, assessorialChangeHistoryFields, assessorialChangeHistoryIndexes, assessorialChangeHistoryForeignKeys)
    assessorialChangeHistoryTable.createTable()
    assessorialChangeHistoryTable.addIndexes()

    return assessorialChangeHistoryTable

def addAssessorialChangeHistory(
    conn : Connection,
    assessorialId : int,
    userId : int,
    dateChanged : str,
    changes : str,
) -> int:
    assessorialChangeHistoryRow = conn.sqlGetInfo('assessorial_change_history', 'id', f"[assessorial_id] = '{assessorialId}' AND [user_id] = '{userId}' AND [date_changed] = '{dateChanged}' AND [changes] = '{changes}'")
    if assessorialChangeHistoryRow:
        return assessorialChangeHistoryRow[0].id
    data = {
        'assessorial_id' : assessorialId,
        'user_id' : userId,
        'date_changed' : dateChanged,
        'changes' : changes,
    }
    conn.sqlInsertRow('assessorial_change_history', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('assessorial_change_history')