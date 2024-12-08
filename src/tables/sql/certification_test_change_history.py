from ...imports import *

certificationTestChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="certification_test_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="user_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL"),
]

certificationTestChangeHistoryIndexes: List[Index] = [
]

certificationTestChangeHistoryForeignKeys: List[ForeignKey] = [
    ForeignKey('certification_test_change_history', 'certification_test_id', 'certification_test', 'id'),
    ForeignKey('certification_test_change_history', 'user_id', 'user', 'id'),
]

def createCertificationTestChangeHistoryTable(conn):
    certificationTestChangeHistoryTable = SqlTable('certification_test_change_history', conn, certificationTestChangeHistoryFields, certificationTestChangeHistoryIndexes, certificationTestChangeHistoryForeignKeys)
    certificationTestChangeHistoryTable.createTable()
    certificationTestChangeHistoryTable.addIndexes()

    return certificationTestChangeHistoryTable

def addCertificationTestChangeHistory(
    conn : Connection,
    certificationTestId : int,
    userId : int,
    dateChanged : str,
    changes : str,
) -> int:
    certificationTestChangeHistoryRow = conn.sqlGetInfo('certification_test_change_history', 'id', f"[certification_test_id] = '{certificationTestId}' AND [user_id] = '{userId}' AND [date_changed] = '{dateChanged}' AND [changes] = '{changes}'")
    if certificationTestChangeHistoryRow:
        return certificationTestChangeHistoryRow[0].id
    data = {
        'certification_test_id' : certificationTestId,
        'user_id' : userId,
        'date_changed' : dateChanged,
        'changes' : changes,
    }
    conn.sqlInsertRow('certification_test_change_history', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('certification_test_change_history')