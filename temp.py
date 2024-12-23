from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

from .src.tables.new.fieldDefinitions import *
from .src.tables.new.indexDefinitions import *
from .src.tables.new.foreignKeyDefinitions import *
from .src.tables.new.conversionFunctions import *

sqlTableDefinitions = {
    'aci_data' :  (aciDataChangeHistoryFields, aciDataChangeHistoryIndexes, aciDataChangeHistoryForeignKeys)
    
}
    
accessTableConversions = {
    'HTC000 G010 T010 Company Info' : {
      'conversionFunction' : convert_HTC000_G010_T010_Company_Info,
      'numErrors' : 0,
      'terminalLineNumber' : 0,
      'conversionStatus' : 'notStarted'
    }
}

def outputTextToTerminal():
    pass

def createSqlTable(connFactory, tableName, tableFields, tableIndexes):
    try:
        localConn : Connection = connFactory()
        localConn.sqlCreateTable(tableName, tableFields)
        for index in tableIndexes:
            localConn.sqlAddIndex(tableName, index.indexType, index.indexFields, index.indexName, index.isUnique)
    except Exception as err:
        sys.stdout.write(f'{err}\n')
    finally:
        localConn.close()
    
def addSqlForeignKey(connFactory, tableName, foreignKeys):
    try:
        localConn : Connection = connFactory()
        for foreignKey in foreignKeys:
            localConn.sqlAddForeignKey(tableName, foreignKey.fromTableField, foreignKey.toTableName, foreignKey.toTableField)
    except Exception as err:
        sys.stdout.write(f'{err}\n')
    finally:
        localConn.close()
    
def convertAccessTable(connFactory, tableName, rows, conversionFunction):
    try:
        localConn : Connection = connFactory()
        if not rows:
          
    except Exception as err:
        sys.stdout.write(f'{err}\n')
    finally:
        localConn.close()

    
def createSqlTables(connFactory, maxThreads):
    with ThreadPoolExecutor(maxThreads) as executor:
        futures = [
            executor.submit(
                createSqlTable, 
                connFactory, 
                tableName,
                definitions[0],
                definitions[1]
            )
            for tableName, definitions in sqlTableDefinitions.items()
        ]

        for future in as_completed(futures):
            future.result()
            
def addSqlForeignKeys(connFactory, maxThreads):
    with ThreadPoolExecutor(maxThreads) as executor:
        futures = [
            executor.submit(
                addSqlForeignKey, 
                connFactory, 
                tableName,
                definitions[2]
            )
            for tableName, definitions in sqlTableDefinitions.items()
        ]

        for future in as_completed(futures):
            future.result()

def convertTables(connFactory, maxThreads):
    with ThreadPoolExecutor(maxThreads) as executor:
        futures = [
            executor.submit(
                tableDetails['conversionFunction'], 
                connFactory, 
                tableName,
                accessTableConversions[tableName]
            )
            for tableName, tableDetails in accessTableConversions.items()
        ]

        for future in as_completed(futures):
            future.result()