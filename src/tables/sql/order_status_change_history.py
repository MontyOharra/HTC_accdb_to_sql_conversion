from ...imports import *

orderStatusChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="order_status_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="user_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL"),
]

orderStatusChangeHistoryIndexes: List[Index] = [
]

orderStatusChangeHistoryForeignKeys: List[ForeignKey] = [
    ForeignKey('order_status_change_history', 'order_status_id', 'order_status', 'id'),
    ForeignKey('order_status_change_history', 'user_id', 'user', 'id'),
]

def createOrderStatusChangeHistoryTable(conn):
    orderStatusChangeHistoryTable = SqlTable('order_status_change_history', conn, orderStatusChangeHistoryFields, orderStatusChangeHistoryIndexes, orderStatusChangeHistoryForeignKeys)
    orderStatusChangeHistoryTable.createTable()
    orderStatusChangeHistoryTable.addIndexes()

    return orderStatusChangeHistoryTable

def addOrderStatusChangeHistory(
    conn : Connection,
    orderStatusId : int,
    userId : int,
    dateChanged : str,
    changes : str,
) -> int:
    orderStatusChangeHistoryRow = conn.sqlGetInfo(
        'order_status_change_history',
        'id',
        whereDetails={
            'order_status_id': orderStatusId,
            'user_id': userId,
            'date_changed': dateChanged,
            'changes': changes
        }
    )
    if orderStatusChangeHistoryRow:
        return orderStatusChangeHistoryRow[0].id
    data = {
        'order_status_id' : orderStatusId,
        'user_id' : userId,
        'date_changed' : dateChanged,
        'changes' : changes,
    }
    conn.sqlInsertRow('order_status_change_history', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('order_status_change_history')