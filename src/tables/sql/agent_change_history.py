from ...imports import *

agentChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="agent_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="user_id", fieldDetails="INTEGER"),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL"),
]

agentChangeHistoryIndexes: List[Index] = [
]

agentChangeHistoryForeignKeys: List[ForeignKey] = [
    ForeignKey('agent_change_history', 'agent_id', 'agent', 'id'),
    ForeignKey('agent_change_history', 'user_id', 'user', 'id'),
]

def createAgentChangeHistoryTable(conn):
    agentChangeHistoryTable = SqlTable('agent_change_history', conn, agentChangeHistoryFields, agentChangeHistoryIndexes, agentChangeHistoryForeignKeys)
    agentChangeHistoryTable.createTable()
    agentChangeHistoryTable.addIndexes()

    return agentChangeHistoryTable

def addAgentChangeHistory(
    conn : Connection,
    agentId : int,
    userId : int,
    dateChanged : str,
    changes : str,
) -> int:
    agentChangeHistoryRow = conn.sqlGetInfo('agent_change_history', 'id', f"[agent_id] = '{agentId}' AND [user_id] = '{userId}' AND [date_changed] = '{dateChanged}' AND [changes] = '{changes}'")
    if agentChangeHistoryRow:
        return agentChangeHistoryRow[0].id
    data = {
        'agent_id' : agentId,
        'user_id' : userId,
        'date_changed' : dateChanged,
        'changes' : changes,
    }
    conn.sqlInsertRow('agent_change_history', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('agent_change_history')