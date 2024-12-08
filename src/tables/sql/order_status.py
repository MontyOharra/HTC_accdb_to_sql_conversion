from ...imports import *

orderStatusFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="order_status_name", fieldDetails="NVARCHAR(25) NOT NULL"),
    Field(fieldName="is_on_manifest", fieldDetails="BIT NOT NULL"),
    Field(fieldName="is_set_to_auto_notify", fieldDetails="BIT NOT NULL"),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL"),
    Field(fieldName="branch_id", fieldDetails="INTEGER NOT NULL"),
]

orderStatusIndexes: List[Index] = [
]

orderStatusForeignKeys: List[ForeignKey] = [
    ForeignKey('order_status', 'branch_id', 'branch', 'id'),
]

def createOrderStatusTable(conn):
    orderStatusTable = SqlTable('order_status', conn, orderStatusFields, orderStatusIndexes, orderStatusForeignKeys)
    orderStatusTable.createTable()
    orderStatusTable.addIndexes()

    return orderStatusTable

def addOrderStatus(
    conn : Connection,
    orderStatusName : str,
    isOnManifest : bool,
    isSetToAutoNotify : bool,
    isActive : bool,
    branchId : int,
) -> int:
    orderStatusRow = conn.sqlGetInfo('order_status', 'id', f"[order_status_name] = '{orderStatusName}' AND [is_on_manifest] = '{isOnManifest}' AND [is_set_to_auto_notify] = '{isSetToAutoNotify}' AND [is_active] = '{isActive}' AND [branch_id] = '{branchId}'")
    if orderStatusRow:
        return orderStatusRow[0].id
    data = {
        'order_status_name' : orderStatusName,
        'is_on_manifest' : isOnManifest,
        'is_set_to_auto_notify' : isSetToAutoNotify,
        'is_active' : isActive,
        'branch_id' : branchId,
    }
    conn.sqlInsertRow('order_status', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('order_status')