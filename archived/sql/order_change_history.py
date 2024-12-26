from ...imports import *

orderChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="order_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="user_id", fieldDetails="INTEGER"),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL"),
]

orderChangeHistoryIndexes: List[Index] = [
]

orderChangeHistoryForeignKeys: List[ForeignKey] = [
    ForeignKey('order_change_history', 'order_id', 'order', 'id'),
    ForeignKey('order_change_history', 'user_id', 'user', 'id'),
]

def createOrderChangeHistoryTable(conn):
    orderChangeHistoryTable = SqlTable('order_change_history', conn, orderChangeHistoryFields, orderChangeHistoryIndexes, orderChangeHistoryForeignKeys)
    orderChangeHistoryTable.createTable()
    orderChangeHistoryTable.addIndexes()

    return orderChangeHistoryTable

def addOrderChangeHistory(
    conn : Connection,
    orderId : int,
    userId : int,
    dateChanged : str,
    changes : str,
) -> int:
    data = {
        'order_id' : orderId,
        'user_id' : userId,
        'date_changed' : dateChanged,
        'changes' : changes,
    }
    conn.sqlInsertRow('order_change_history', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('order_change_history')