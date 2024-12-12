from ...imports import *

certificationTestFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="certification_name", fieldDetails="NVARCHAR(63) NOT NULL"),
    Field(fieldName="certification_test_trainer_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL"),
]

certificationTestIndexes: List[Index] = [
]

certificationTestForeignKeys: List[ForeignKey] = [
    ForeignKey('certification_test', 'certification_test_trainer_id', 'certification_test_trainer', 'id'),
]

def createCertificationTestTable(conn):
    certificationTestTable = SqlTable('certification_test', conn, certificationTestFields, certificationTestIndexes, certificationTestForeignKeys)
    certificationTestTable.createTable()
    certificationTestTable.addIndexes()

    return certificationTestTable

def addCertificationTest(
    conn : Connection,
    certificationTestId : id,
    certificationName : str,
    certificationTestTrainerId : int,
    isActive : bool,
) -> int:
    certificationTestRow = conn.sqlGetInfo(
        'certification_test',
        'id',
        whereDetails={
            'certification_name': certificationName,
            'certification_test_trainer_id': certificationTestTrainerId,
            'is_active': isActive
        }
    )
    if certificationTestRow:
        return certificationTestRow[0].id

    data = {
        'certification_name': certificationName,
        'certification_test_trainer_id': certificationTestTrainerId,
        'is_active': isActive,
    }
    conn.sqlInsertRow('certification_test', data, insertId=certificationTestId)
    conn.commit()

    return conn.sqlGetLastIdCreated('certification_test')