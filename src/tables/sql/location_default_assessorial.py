from ...imports import *

locationDefaultAssessorialFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="location_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="assessorial_id", fieldDetails="INTEGER NOT NULL"),
]

locationDefaultAssessorialIndexes: List[Index] = [
]

locationDefaultAssessorialForeignKeys: List[ForeignKey] = [
    ForeignKey('location_default_assessorial', 'location_id', 'location', 'id'),
    ForeignKey('location_default_assessorial', 'assessorial_id', 'assessorial', 'id'),
]

def createLocationDefaultAssessorialTable(conn):
    locationDefaultAssessorialTable = SqlTable('location_default_assessorial', conn, locationDefaultAssessorialFields, locationDefaultAssessorialIndexes, locationDefaultAssessorialForeignKeys)
    locationDefaultAssessorialTable.createTable()
    locationDefaultAssessorialTable.addIndexes()

    return locationDefaultAssessorialTable

def addLocationDefaultAssessorial(
    conn : Connection,
    locationId : int,
    assessorialId : int,
) -> int:
    locationDefaultAssessorialRow = conn.sqlGetInfo('location_default_assessorial', 'id', f"[location_id] = '{locationId}' AND [assessorial_id] = '{assessorialId}'")
    if locationDefaultAssessorialRow:
        return locationDefaultAssessorialRow[0].id
    data = {
        'location_id' : locationId,
        'assessorial_id' : assessorialId,
    }
    conn.sqlInsertRow('location_default_assessorial', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('location_default_assessorial')