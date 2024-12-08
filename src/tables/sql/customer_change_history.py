from ...imports import *

customerChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="customer_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="user_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL"),
]

customerChangeHistoryIndexes: List[Index] = [
]

customerChangeHistoryForeignKeys: List[ForeignKey] = [
    ForeignKey('customer_change_history', 'customer_id', 'customer', 'id'),
    ForeignKey('customer_change_history', 'user_id', 'user', 'id'),
]

def createCustomerChangeHistoryTable(conn):
    customerChangeHistoryTable = SqlTable('customer_change_history', conn, customerChangeHistoryFields, customerChangeHistoryIndexes, customerChangeHistoryForeignKeys)
    customerChangeHistoryTable.createTable()
    customerChangeHistoryTable.addIndexes()

    return customerChangeHistoryTable

def addCustomerChangeHistory(
    conn : Connection,
    customerId : int,
    userId : int,
    dateChanged : str,
    changes : str,
) -> int:
    customerChangeHistoryRow = conn.sqlGetInfo('customer_change_history', 'id', f"[customer_id] = '{customerId}' AND [user_id] = '{userId}' AND [date_changed] = '{dateChanged}' AND [changes] = '{changes}'")
    if customerChangeHistoryRow:
        return customerChangeHistoryRow[0].id
    data = {
        'customer_id' : customerId,
        'user_id' : userId,
        'date_changed' : dateChanged,
        'changes' : changes,
    }
    conn.sqlInsertRow('customer_change_history', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('customer_change_history')