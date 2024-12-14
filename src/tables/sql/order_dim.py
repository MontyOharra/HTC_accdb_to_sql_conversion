from ...imports import *

orderDimFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="order_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="unit_type", fieldDetails="NVARCHAR(15)"),
    Field(fieldName="unit_quantity", fieldDetails="INTEGER"),
    Field(fieldName="unit_weight", fieldDetails="INTEGER"),
    Field(fieldName="dim_height", fieldDetails="INTEGER"),
    Field(fieldName="dim_width", fieldDetails="INTEGER"),
    Field(fieldName="dim_length", fieldDetails="INTEGER"),
    Field(fieldName="dim_weight", fieldDetails="DECIMAL(20,10)"),
]

orderDimIndexes: List[Index] = [
]

orderDimForeignKeys: List[ForeignKey] = [
    ForeignKey('order_dim', 'order_id', 'order', 'id'),
]

def createOrderDimTable(conn):
    orderDimTable = SqlTable('order_dim', conn, orderDimFields, orderDimIndexes, orderDimForeignKeys)
    orderDimTable.createTable()
    orderDimTable.addIndexes()

    return orderDimTable

def addOrderDim(
    conn : Connection,
    orderId : int,
    unitType : str,
    unitQuantity : int,
    unitWeight : int,
    dimHeight : int,
    dimWidth : int,
    dimLength : int,
    dimWeight : float,
) -> int:
    orderDimRow = conn.sqlGetInfo(
        'order_dim',
        'id',
        whereDetails={
            'order_id': orderId,
            'unit_type': unitType,
            'unit_quantity': unitQuantity,
            'unit_weight': unitWeight,
            'dim_height': dimHeight,
            'dim_width': dimWidth,
            'dim_length': dimLength,
            'dim_weight': dimWeight
        }
    )
    if orderDimRow:
        return orderDimRow[0].id

    data = {
        'order_id' : orderId,
        'unit_type' : unitType,
        'unit_quantity' : unitQuantity,
        'unit_weight' : unitWeight,
        'dim_height' : dimHeight,
        'dim_width' : dimWidth,
        'dim_length' : dimLength,
        'dim_weight' : dimWeight,
    }
    conn.sqlInsertRow('order_dim', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('order_dim')