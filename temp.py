from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

from .src.tables.new.fieldDefinitions import *
from .src.tables.new.indexDefinitions import *
from .src.tables.new.foreignKeyDefinitions import *

sqlTableDefinitions = {
    'aci_data' : (aciDataChangeHistoryFields, aciDataChangeHistoryIndexes, aciDataChangeHistoryForeignKeys)
}

def createSqlTable(connFactory, tableName, tableFields, tableIndexes):
    localConn : Connection = connFactory()
    localConn.sqlCreateTable(tableName, tableFields)
    for index in tableIndexes:
        localConn.sqlAddIndex(tableName, index.indexType, index.indexFields, index.indexName, index.isUnique)

    localConn.close()
    
def addSqlForeignKey(connFactory, tableName, foreignKeys):
    localConn : Connection = connFactory()
    for foreignKey in foreignKeys:
        localConn.sqlAddForeignKey(tableName, foreignKey.fromTableField, foreignKey.toTableName, foreignKey.toTableField)
        
    localConn.close()
    
def createSqlTables(connFactory, maxThreads):
    with ThreadPoolExecutor(maxThreads) as executor:
        futures = [
            executor.submit(
                createSqlTable, 
                connFactory, createSqlServerTableTask
            )
            for createSqlServerTableTask in createSqlServerTableTasks
        ]

        for future in as_completed(futures):
            future.result()