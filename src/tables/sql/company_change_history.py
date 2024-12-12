from ...imports import *

companyChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="company_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="user_id", fieldDetails="INTEGER"),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL"),
]

companyChangeHistoryIndexes: List[Index] = [
]

companyChangeHistoryForeignKeys: List[ForeignKey] = [
    ForeignKey('company_change_history', 'company_id', 'company', 'id'),
    ForeignKey('company_change_history', 'user_id', 'user', 'id'),
]

def createCompanyChangeHistoryTable(conn):
    companyChangeHistoryTable = SqlTable('company_change_history', conn, companyChangeHistoryFields, companyChangeHistoryIndexes, companyChangeHistoryForeignKeys)
    companyChangeHistoryTable.createTable()
    companyChangeHistoryTable.addIndexes()

    return companyChangeHistoryTable

def addCompanyChangeHistory(
    conn : Connection,
    companyId : int,
    userId : int,
    dateChanged : str,
    changes : str,
) -> int:
    companyChangeHistoryRow = conn.sqlGetInfo('company_change_history', 'id', f"[company_id] = '{companyId}' AND [user_id] = '{userId}' AND [date_changed] = '{dateChanged}' AND [changes] = '{changes}'")
    if companyChangeHistoryRow:
        return companyChangeHistoryRow[0].id
    data = {
        'company_id' : companyId,
        'user_id' : userId,
        'date_changed' : dateChanged,
        'changes' : changes,
    }
    conn.sqlInsertRow('company_change_history', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('company_change_history')