from ...imports import *

rateChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="rate_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="user_id", fieldDetails="INTEGER"),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL"),
]

rateChangeHistoryIndexes: List[Index] = [
]

rateChangeHistoryForeignKeys: List[ForeignKey] = [
    ForeignKey('rate_change_history', 'rate_id', 'rate', 'id'),
    ForeignKey('rate_change_history', 'user_id', 'user', 'id'),
]

def createRateChangeHistoryTable(conn):
    rateChangeHistoryTable = SqlTable('rate_change_history', conn, rateChangeHistoryFields, rateChangeHistoryIndexes, rateChangeHistoryForeignKeys)
    rateChangeHistoryTable.createTable()
    rateChangeHistoryTable.addIndexes()

    return rateChangeHistoryTable

def addRateChangeHistory(
    conn : Connection,
    rateId : int,
    userId : int,
    dateChanged : str,
    changes : str,
) -> int:

    data = {
        'rate_id' : rateId,
        'user_id' : userId,
        'date_changed' : dateChanged,
        'changes' : changes,
    }
    conn.sqlInsertRow('rate_change_history', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('rate_change_history')