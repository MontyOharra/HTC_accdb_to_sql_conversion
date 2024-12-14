from ...imports import *

branchChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="branch_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="user_id", fieldDetails="INTEGER"),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL"),
]

branchChangeHistoryIndexes: List[Index] = [
]

branchChangeHistoryForeignKeys: List[ForeignKey] = [
    ForeignKey('branch_change_history', 'branch_id', 'branch', 'id'),
    ForeignKey('branch_change_history', 'user_id', 'user', 'id'),
]

def createBranchChangeHistoryTable(conn):
    branchChangeHistoryTable = SqlTable('branch_change_history', conn, branchChangeHistoryFields, branchChangeHistoryIndexes, branchChangeHistoryForeignKeys)
    branchChangeHistoryTable.createTable()
    branchChangeHistoryTable.addIndexes()

    return branchChangeHistoryTable

def addBranchChangeHistory(
    conn : Connection,
    branchId : int,
    userId : int,
    dateChanged : str,
    changes : str,
) -> int:

    data = {
        'branch_id' : branchId,
        'user_id' : userId,
        'date_changed' : dateChanged,
        'changes' : changes,
    }
    conn.sqlInsertRow('branch_change_history', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('branch_change_history')