from ...imports import *

customerDefaultAssessorialFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="customer_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="assessorial_id", fieldDetails="INTEGER NOT NULL"),
]

customerDefaultAssessorialIndexes: List[Index] = [
]

customerDefaultAssessorialForeignKeys: List[ForeignKey] = [
    ForeignKey('customer_default_assessorial', 'customer_id', 'customer', 'id'),
    ForeignKey('customer_default_assessorial', 'assessorial_id', 'assessorial', 'id'),
]

def createCustomerDefaultAssessorialTable(conn):
    customerDefaultAssessorialTable = SqlTable('customer_default_assessorial', conn, customerDefaultAssessorialFields, customerDefaultAssessorialIndexes, customerDefaultAssessorialForeignKeys)
    customerDefaultAssessorialTable.createTable()
    customerDefaultAssessorialTable.addIndexes()

    return customerDefaultAssessorialTable

def addCustomerDefaultAssessorial(
    conn : Connection,
    customerId : int,
    assessorialId : int,
) -> int:
    customerDefaultAssessorialRow = conn.sqlGetInfo(
        'customer_default_assessorial',
        'id',
        whereDetails={
            'customer_id': customerId,
            'assessorial_id': assessorialId
        }
    )
    if customerDefaultAssessorialRow:
        return customerDefaultAssessorialRow[0].id

    data = {
        'customer_id' : customerId,
        'assessorial_id' : assessorialId,
    }
    conn.sqlInsertRow('customer_default_assessorial', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('customer_default_assessorial')