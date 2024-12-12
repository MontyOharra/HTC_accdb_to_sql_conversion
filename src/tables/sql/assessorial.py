from ...imports import *

assessorialFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="branch_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="assessorial_name", fieldDetails="NVARCHAR(31) NOT NULL"),
    Field(fieldName="min_charge", fieldDetails="MONEY NOT NULL"),
    Field(fieldName="basis_type", fieldDetails="nvarchar(255) NOT NULL CHECK ([basis_type] IN ('fixed', 'weight', 'prompt'))"),
    Field(fieldName="basis_portion", fieldDetails="FLOAT NOT NULL"),
    Field(fieldName="basis_rate", fieldDetails="MONEY"),
    Field(fieldName="user_prompt", fieldDetails="NVARCHAR(127)"),
    Field(fieldName="date_created", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="notes", fieldDetails="NTEXT"),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL DEFAULT (1)"),
]

assessorialIndexes: List[Index] = [
]

assessorialForeignKeys: List[ForeignKey] = [
    ForeignKey('assessorial', 'branch_id', 'branch', 'id'),
]

def createAssessorialTable(conn):
    assessorialTable = SqlTable('assessorial', conn, assessorialFields, assessorialIndexes, assessorialForeignKeys)
    assessorialTable.createTable()
    assessorialTable.addIndexes()

    return assessorialTable

def addAssessorial(
    conn : Connection,
    assessorialId : int,
    branchId : int,
    assessorialName : str,
    minCharge : float,
    basisType : float,
    basisPortion : float,
    basisRate : float,
    userPrompt : str,
    dateCreated : str,
    notes : str,
    isActive : bool,
) -> int:
    assessorialRow = conn.sqlGetInfo(
        'assessorial',
        'id',
        whereDetails={
            'branch_id': branchId,
            'assessorial_name': assessorialName,
            'min_charge': minCharge,
            'basis_type': basisType,
            'basis_portion': basisPortion,
            'basis_rate': basisRate,
            'user_prompt': userPrompt,
            'date_created': dateCreated,
            'notes': notes,
            'is_active': isActive
        }
    )
    if assessorialRow:
        return assessorialRow[0].id
    data = {
        'branch_id' : branchId,
        'assessorial_name' : assessorialName,
        'min_charge' : minCharge,
        'basis_type' : basisType,
        'basis_portion' : basisPortion,
        'basis_rate' : basisRate,
        'user_prompt' : userPrompt,
        'date_created' : dateCreated,
        'notes' : notes,
        'is_active' : isActive,
    }
    conn.sqlInsertRow('assessorial', data, insertId=assessorialId)
    conn.commit()

    return conn.sqlGetLastIdCreated('assessorial')

def getAssessorialFields()