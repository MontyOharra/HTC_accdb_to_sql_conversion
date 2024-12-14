from ...imports import *

orderDriverFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="order_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="driver_user_id", fieldDetails="INTEGER"),
    Field(fieldName="order_leg", fieldDetails="NVARCHAR(1)"),
    Field(fieldName="driver_role", fieldDetails="NVARCHAR(1)"),
]

orderDriverIndexes: List[Index] = [
]

orderDriverForeignKeys: List[ForeignKey] = [
    ForeignKey('order_driver', 'order_id', 'order', 'id'),
    ForeignKey('order_driver', 'driver_user_id', 'user', 'id'),
]

def createOrderDriverTable(conn):
    orderDriverTable = SqlTable('order_driver', conn, orderDriverFields, orderDriverIndexes, orderDriverForeignKeys)
    orderDriverTable.createTable()
    orderDriverTable.addIndexes()

    return orderDriverTable

def addOrderDriver(
    conn : Connection,
    orderId : int,
    driverUserId : int,
    orderLeg : str,
    driverRole : str,
) -> int:
    orderDriverRow = conn.sqlGetInfo(
        'order_driver',
        'id',
        whereDetails={
            'order_id': orderId,
            'driver_user_id' : driverUserId,
            'order_leg': orderLeg,
            'driver_role': driverRole
        }
    )
    if orderDriverRow:
        return orderDriverRow[0].id

    data = {
        'order_id' : orderId,
        'order_leg' : orderLeg,
        'driver_role' : driverRole,
    }
    conn.sqlInsertRow('order_driver', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('order_driver')