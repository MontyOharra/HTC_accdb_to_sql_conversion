from ...imports import *

orderTypeFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="order_type_name", fieldDetails="NVARCHAR(31) NOT NULL"),
]

orderTypeIndexes: List[Index] = [
]

orderTypeForeignKeys: List[ForeignKey] = [
]

def createOrderTypeTable(conn):
    orderTypeTable = SqlTable('order_type', conn, orderTypeFields, orderTypeIndexes, orderTypeForeignKeys)
    orderTypeTable.createTable()
    orderTypeTable.addIndexes()

    return orderTypeTable

def addOrderType(
    conn : Connection,
    orderTypeName : str,
) -> int:
    orderTypeRow = conn.sqlGetInfo('order_type', 'id', f"[order_type_name] = '{orderTypeName}'")
    if orderTypeRow:
        return orderTypeRow[0].id
    data = {
        'order_type_name' : orderTypeName,
    }
    conn.sqlInsertRow('order_type', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('order_type')