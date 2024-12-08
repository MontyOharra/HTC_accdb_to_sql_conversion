from ...imports import *

rateFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="rate_name", fieldDetails="NVARCHAR(31) NOT NULL"),
    Field(fieldName="branch_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="is_default", fieldDetails="BIT NOT NULL DEFAULT (0)"),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL DEFAULT (1)"),
    Field(fieldName="date_added", fieldDetails="DATETIME2"),
    Field(fieldName="added_by_user_id", fieldDetails="INTEGER"),
]

rateIndexes: List[Index] = [
]

rateForeignKeys: List[ForeignKey] = [
    ForeignKey('rate', 'branch_id', 'branch', 'id'),
    ForeignKey('rate', 'added_by_user_id', 'user', 'id'),
]

def createRateTable(conn):
    rateTable = SqlTable('rate', conn, rateFields, rateIndexes, rateForeignKeys)
    rateTable.createTable()
    rateTable.addIndexes()

    return rateTable

def addRate(
    conn : Connection,
    rateName : str,
    branchId : int,
    isDefault : bool,
    isActive : bool,
    dateAdded : str,
    addedByUserId : int,
) -> int:
    rateRow = conn.sqlGetInfo('rate', 'id', f"[rate_name] = '{rateName}' AND [branch_id] = '{branchId}' AND [is_default] = '{isDefault}' AND [is_active] = '{isActive}' AND [date_added] = '{dateAdded}' AND [added_by_user_id] = '{addedByUserId}'")
    if rateRow:
        return rateRow[0].id
    data = {
        'rate_name' : rateName,
        'branch_id' : branchId,
        'is_default' : isDefault,
        'is_active' : isActive,
        'date_added' : dateAdded,
        'added_by_user_id' : addedByUserId,
    }
    conn.sqlInsertRow('rate', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('rate')