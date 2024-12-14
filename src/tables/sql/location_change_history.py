from ...imports import *

locationChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="location_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="user_id", fieldDetails="INTEGER"),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL"),
]

locationChangeHistoryIndexes: List[Index] = [
]

locationChangeHistoryForeignKeys: List[ForeignKey] = [
    ForeignKey('location_change_history', 'location_id', 'location', 'id'),
    ForeignKey('location_change_history', 'user_id', 'user', 'id'),
]

def createLocationChangeHistoryTable(conn):
    locationChangeHistoryTable = SqlTable('location_change_history', conn, locationChangeHistoryFields, locationChangeHistoryIndexes, locationChangeHistoryForeignKeys)
    locationChangeHistoryTable.createTable()
    locationChangeHistoryTable.addIndexes()

    return locationChangeHistoryTable

def addLocationChangeHistory(
    conn : Connection,
    locationId : int,
    userId : int,
    dateChanged : str,
    changes : str,
) -> int:
    locationChangeHistoryRow = conn.sqlGetInfo(
        'location_change_history',
        'id',
        whereDetails={
            'location_id': locationId,
            'user_id': userId,
            'date_changed': dateChanged,
            'changes': changes
        }
    )
    if locationChangeHistoryRow:
        return locationChangeHistoryRow[0].id
    data = {
        'location_id' : locationId,
        'user_id' : userId,
        'date_changed' : dateChanged,
        'changes' : changes,
    }
    conn.sqlInsertRow('location_change_history', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('location_change_history')