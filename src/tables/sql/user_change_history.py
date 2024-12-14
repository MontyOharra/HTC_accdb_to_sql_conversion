from ...imports import *

userChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="user_changed_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="user_id", fieldDetails="INTEGER"),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL"),
]

userChangeHistoryIndexes: List[Index] = [
]

userChangeHistoryForeignKeys: List[ForeignKey] = [
    ForeignKey('user_change_history', 'user_changed_id', 'user', 'id'),
    ForeignKey('user_change_history', 'user_id', 'user', 'id'),
]

def createUserChangeHistoryTable(conn):
    userChangeHistoryTable = SqlTable('user_change_history', conn, userChangeHistoryFields, userChangeHistoryIndexes, userChangeHistoryForeignKeys)
    userChangeHistoryTable.createTable()
    userChangeHistoryTable.addIndexes()

    return userChangeHistoryTable

def addUserChangeHistory(
    conn : Connection,
    userChangedId : int,
    userId : int,
    dateChanged : str,
    changes : str,
) -> int:

    data = {
        'user_changed_id' : userChangedId,
        'user_id' : userId,
        'date_changed' : dateChanged,
        'changes' : changes,
    }
    conn.sqlInsertRow('user_change_history', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('user_change_history')