from ...imports import *

orderAttachmentFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="order_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="attachment_path", fieldDetails="NVARCHAR(MAX)"),
    Field(fieldName="file_size", fieldDetails="DECIMAL(30,15)"),
]

orderAttachmentIndexes: List[Index] = [
]

orderAttachmentForeignKeys: List[ForeignKey] = [
    ForeignKey('order_attachment', 'order_id', 'order', 'id'),
]

def createOrderAttachmentTable(conn):
    orderAttachmentTable = SqlTable('order_attachment', conn, orderAttachmentFields, orderAttachmentIndexes, orderAttachmentForeignKeys)
    orderAttachmentTable.createTable()
    orderAttachmentTable.addIndexes()

    return orderAttachmentTable

def addOrderAttachment(
    conn : Connection,
    orderId : int,
    attachmentPath : str,
    fileSize : float,
) -> int:
    orderAttachmentRow = conn.sqlGetInfo(
        'order_attachment',
        'id',
        whereDetails={
            'order_id': orderId,
            'attachment_path': attachmentPath,
            'file_size': fileSize
        }
    )
    if orderAttachmentRow:
        return orderAttachmentRow[0].id
    data = {
        'order_id' : orderId,
        'attachment_path' : attachmentPath,
        'file_size' : fileSize,
    }
    conn.sqlInsertRow('order_attachment', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('order_attachment')