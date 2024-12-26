from ...imports import *

holidayFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="holiday_name", fieldDetails="NVARCHAR(31) NOT NULL"),
    Field(fieldName="holiday_date", fieldDetails="DATETIME2 NOT NULL"),
]

holidayIndexes: List[Index] = [
]

holidayForeignKeys: List[ForeignKey] = [
]

def createHolidayTable(conn):
    holidayTable = SqlTable('holiday', conn, holidayFields, holidayIndexes, holidayForeignKeys)
    holidayTable.createTable()
    holidayTable.addIndexes()

    return holidayTable

def addHoliday(
    conn : Connection,
    holidayName : str,
    holidayDate : str,
) -> int:
    holidayRow = conn.sqlGetInfo(
        'holiday',
        'id',
        whereDetails={
            'holiday_name': ''.join(["''" if x == "'" else x for x in holidayName]),
            'holiday_date': holidayDate
        }
    )
    if holidayRow:
        return holidayRow[0].id

    data = {
        'holiday_name': holidayName,
        'holiday_date': holidayDate,
    }
    conn.sqlInsertRow('holiday', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('holiday')