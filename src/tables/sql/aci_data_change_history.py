from ...imports import *

aciDataChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="aci_data_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="user_id", fieldDetails="INTEGER"),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL"),
]

aciDataChangeHistoryIndexes: List[Index] = [
]

aciDataChangeHistoryForeignKeys: List[ForeignKey] = [
    ForeignKey('aci_data_change_history', 'aci_data_id', 'aci_data', 'id'),
    ForeignKey('aci_data_change_history', 'user_id', 'user', 'id'),
]

def createAciDataChangeHistoryTable(conn):
    aciDataChangeHistoryTable = SqlTable('aci_data_change_history', conn, aciDataChangeHistoryFields, aciDataChangeHistoryIndexes, aciDataChangeHistoryForeignKeys)
    aciDataChangeHistoryTable.createTable()
    aciDataChangeHistoryTable.addIndexes()

    return aciDataChangeHistoryTable

def addAciDataChangeHistory(
    conn : Connection,
    aciDataId : int,
    userId : int,
    dateChanged : str,
    changes : str,
) -> int:
    aciDataChangeHistoryRow = conn.sqlGetInfo(
        'aci_data_change_history',
        'id',
        whereDetails={
            'aci_data_id': aciDataId,
            'user_id': userId,
            'date_changed': dateChanged,
            'changes': changes
        }
    )
    if aciDataChangeHistoryRow:
        return aciDataChangeHistoryRow[0].id
    data = {
        'aci_data_id' : aciDataId,
        'user_id' : userId,
        'date_changed' : dateChanged,
        'changes' : changes,
    }
    conn.sqlInsertRow('aci_data_change_history', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('aci_data_change_history')