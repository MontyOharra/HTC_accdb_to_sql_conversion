from ...imports import *

agentCertificationTestFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="agent_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="certification_test_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="date_tested", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="test_score", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL DEFAULT (1)"),
]

agentCertificationTestIndexes: List[Index] = [
]

agentCertificationTestForeignKeys: List[ForeignKey] = [
    ForeignKey('agent_certification_test', 'agent_id', 'agent', 'id'),
    ForeignKey('agent_certification_test', 'certification_test_id', 'certification_test', 'id'),
]

def createAgentCertificationTestTable(conn):
    agentCertificationTestTable = SqlTable('agent_certification_test', conn, agentCertificationTestFields, agentCertificationTestIndexes, agentCertificationTestForeignKeys)
    agentCertificationTestTable.createTable()
    agentCertificationTestTable.addIndexes()

    return agentCertificationTestTable

def addAgentCertificationTest(
    conn : Connection,
    agentId : int,
    certificationTestId : int,
    dateTested : str,
    testScore : int,
    isActive : bool,
) -> int:
    agentCertificationTestRow = conn.sqlGetInfo(
        'agent_certification_test',
        'id',
        whereDetails={
            'agent_id': agentId,
            'certification_test_id': certificationTestId,
            'date_tested': dateTested,
            'test_score': testScore,
            'is_active': isActive
        }
    )
    if agentCertificationTestRow:
        return agentCertificationTestRow[0].id
    data = {
        'agent_id' : agentId,
        'certification_test_id' : certificationTestId,
        'date_tested' : dateTested,
        'test_score' : testScore,
        'is_active' : isActive,
    }
    conn.sqlInsertRow('agent_certification_test', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('agent_certification_test')