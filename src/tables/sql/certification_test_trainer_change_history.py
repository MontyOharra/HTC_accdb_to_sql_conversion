from ...imports import *

certificationTestTrainerChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="certification_test_trainer_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="user_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL"),
]

certificationTestTrainerChangeHistoryIndexes: List[Index] = [
]

certificationTestTrainerChangeHistoryForeignKeys: List[ForeignKey] = [
    ForeignKey('certification_test_trainer_change_history', 'certification_test_trainer_id', 'certification_test_trainer', 'id'),
    ForeignKey('certification_test_trainer_change_history', 'user_id', 'user', 'id'),
]

def createCertificationTestTrainerChangeHistoryTable(conn):
    certificationTestTrainerChangeHistoryTable = SqlTable('certification_test_trainer_change_history', conn, certificationTestTrainerChangeHistoryFields, certificationTestTrainerChangeHistoryIndexes, certificationTestTrainerChangeHistoryForeignKeys)
    certificationTestTrainerChangeHistoryTable.createTable()
    certificationTestTrainerChangeHistoryTable.addIndexes()

    return certificationTestTrainerChangeHistoryTable

def addCertificationTestTrainerChangeHistory(
    conn : Connection,
    certificationTestTrainerId : int,
    userId : int,
    dateChanged : str,
    changes : str,
) -> int:
    certificationTestTrainerChangeHistoryRow = conn.sqlGetInfo('certification_test_trainer_change_history', 'id', f"[certification_test_trainer_id] = '{certificationTestTrainerId}' AND [user_id] = '{userId}' AND [date_changed] = '{dateChanged}' AND [changes] = '{changes}'")
    if certificationTestTrainerChangeHistoryRow:
        return certificationTestTrainerChangeHistoryRow[0].id
    data = {
        'certification_test_trainer_id' : certificationTestTrainerId,
        'user_id' : userId,
        'date_changed' : dateChanged,
        'changes' : changes,
    }
    conn.sqlInsertRow('certification_test_trainer_change_history', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('certification_test_trainer_change_history')