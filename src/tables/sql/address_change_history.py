from ...imports import *

addressChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="address_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="user_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL"),
]

addressChangeHistoryIndexes: List[Index] = [
]

addressChangeHistoryForeignKeys: List[ForeignKey] = [
    ForeignKey('address_change_history', 'address_id', 'address', 'id'),
    ForeignKey('address_change_history', 'user_id', 'user', 'id'),
]

def createAddressChangeHistoryTable(conn):
    addressChangeHistoryTable = SqlTable('address_change_history', conn, addressChangeHistoryFields, addressChangeHistoryIndexes, addressChangeHistoryForeignKeys)
    addressChangeHistoryTable.createTable()
    addressChangeHistoryTable.addIndexes()

    return addressChangeHistoryTable

def addAddressChangeHistory(
    conn : Connection,
    addressId : int,
    userId : int,
    dateChanged : str,
    changes : str,
) -> int:
    addressChangeHistoryRow = conn.sqlGetInfo('address_change_history', 'id', f"[address_id] = '{addressId}' AND [user_id] = '{userId}' AND [date_changed] = '{dateChanged}' AND [changes] = '{changes}'")
    if addressChangeHistoryRow:
        return addressChangeHistoryRow[0].id
    data = {
        'address_id' : addressId,
        'user_id' : userId,
        'date_changed' : dateChanged,
        'changes' : changes,
    }
    conn.sqlInsertRow('address_change_history', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('address_change_history')