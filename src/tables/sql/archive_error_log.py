from ...imports import *

archiveErrorLogFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="order_id", fieldDetails="INTEGER"),
    Field(fieldName="archive_date", fieldDetails="DATETIME2"),
    Field(fieldName="user_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="details", fieldDetails="NTEXT"),
]

archiveErrorLogIndexes: List[Index] = [
]

archiveErrorLogForeignKeys: List[ForeignKey] = [
    ForeignKey('archive_error_log', 'order_id', 'order', 'id'),
    ForeignKey('archive_error_log', 'user_id', 'user', 'id'),
]

def createArchiveErrorLogTable(conn):
    archiveErrorLogTable = SqlTable('archive_error_log', conn, archiveErrorLogFields, archiveErrorLogIndexes, archiveErrorLogForeignKeys)
    archiveErrorLogTable.createTable()
    archiveErrorLogTable.addIndexes()

    return archiveErrorLogTable

def addArchiveErrorLog(
    conn : Connection,
    orderId : int,
    archiveDate : str,
    userId : int,
    details : int,
) -> int:
    archiveErrorLogRow = conn.sqlGetInfo('archive_error_log', 'id', f"[order_id] = '{orderId}' AND [archive_date] = '{archiveDate}' AND [user_id] = '{userId}' AND [details] = '{details}'")
    if archiveErrorLogRow:
        return archiveErrorLogRow[0].id
    data = {
        'order_id' : orderId,
        'archive_date' : archiveDate,
        'user_id' : userId,
        'details' : details,
    }
    conn.sqlInsertRow('archive_error_log', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('archive_error_log')