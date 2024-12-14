from ...imports import *

orderAssessorialFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="order_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="assessorial_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="parent_type", fieldDetails="NVARCHAR(15) NOT NULL"),
    Field(fieldName="basis_count", fieldDetails="DECIMAL(6,2)"),
    Field(fieldName="total_charge", fieldDetails="MONEY"),
]

orderAssessorialIndexes: List[Index] = [
]

orderAssessorialForeignKeys: List[ForeignKey] = [
    ForeignKey('order_assessorial', 'order_id', 'order', 'id'),
    ForeignKey('order_assessorial', 'assessorial_id', 'assessorial', 'id'),
]

def createOrderAssessorialTable(conn):
    orderAssessorialTable = SqlTable('order_assessorial', conn, orderAssessorialFields, orderAssessorialIndexes, orderAssessorialForeignKeys)
    orderAssessorialTable.createTable()
    orderAssessorialTable.addIndexes()

    return orderAssessorialTable

def addOrderAssessorial(
    conn : Connection,
    orderId : int,
    assessorialId : int,
    parentType : str,
    basisCount : float,
    totalCharge : float,
) -> int:
    orderAssessorialRow = conn.sqlGetInfo(
        'order_assessorial',
        'id',
        whereDetails={
            'order_id': orderId,
            'assessorial_id': assessorialId,
            'parent_type': parentType,
            'basis_count': basisCount,
            'total_charge': totalCharge
        }
    )
    if orderAssessorialRow:
        return orderAssessorialRow[0].id

    data = {
        'order_id' : orderId,
        'assessorial_id' : assessorialId,
        'parent_type' : parentType,
        'basis_count' : basisCount,
        'total_charge' : totalCharge,
    }
    conn.sqlInsertRow('order_assessorial', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('order_assessorial')