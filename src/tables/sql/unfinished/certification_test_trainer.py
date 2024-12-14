from ...imports import *

certificationTestTrainerFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="trainer_name", fieldDetails="NVARCHAR(63)"),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL DEFAULT (1)"),
]

certificationTestTrainerIndexes: List[Index] = [
]

certificationTestTrainerForeignKeys: List[ForeignKey] = [
]

def createCertificationTestTrainerTable(conn):
    certificationTestTrainerTable = SqlTable('certification_test_trainer', conn, certificationTestTrainerFields, certificationTestTrainerIndexes, certificationTestTrainerForeignKeys)
    certificationTestTrainerTable.createTable()
    certificationTestTrainerTable.addIndexes()

    return certificationTestTrainerTable

def addCertificationTestTrainer(
    conn : Connection,
    trainerName : str,
    isActive : bool,
) -> int:
    certificationTestTrainerRow = conn.sqlGetInfo(
        'certification_test_trainer',
        'id',
        whereDetails={
            'trainer_name': trainerName,
            'is_active': isActive
        }
    )
    if certificationTestTrainerRow:
        return certificationTestTrainerRow[0].id

    data = {
        'trainer_name' : trainerName,
        'is_active' : isActive,
    }
    conn.sqlInsertRow('certification_test_trainer', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('certification_test_trainer')