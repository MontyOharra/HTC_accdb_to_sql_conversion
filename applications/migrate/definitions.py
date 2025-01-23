from src.utils.conversionHelpers import generateAccessDbNameCache

from .conversionDefinitions.tablesToMigrate import tablesToMigrate as tablesToMigrateDefault
from typing import Dict
from src.types.types import Field

from collections.abc import Callable

def getMigrationDefinitions(connFactories : Dict[str, Callable], tablesToMigrate=tablesToMigrateDefault):
    accessDbNameCache = generateAccessDbNameCache(tablesToMigrate)
    
    sqlTableDefinitions = {}
    accessConversionDefinitions = {}
    for tableName in tablesToMigrate:
        conn = connFactories[accessDbNameCache[tableName]]()
        sqlTableDefinitions[tableName] = (
            getSqlTableFields(conn, tableName), 
            getSqlTableIndexes(conn, tableName), 
            getSqlTableForeignKeys(conn, tableName)
        )
        accessConversionDefinitions[tableName] = getAccessConversionFunction(conn, tableName)
    
    return sqlTableDefinitions, accessConversionDefinitions


def getSqlTableFields(conn, accessTableName):
    structureDetails = conn.getTableStructure(accessTableName)
    fields = []
    
    for column in structureDetails['columnsInfo']:
        fields.append(Field(column['name'], column['details'] + ' NOT NULL' if column['details'][-8:] != 'NOT NULL' else column['details']))
    
    return fields

def getSqlTableIndexes(conn, accessTableName):
    return []

def getSqlTableForeignKeys(conn, accessTableName):
    return []

def getAccessConversionFunction(conn, accessTableName):
    columnNames = [column['name'] for column in conn.getTableStructure(accessTableName)['columnsInfo']]

    def conversionFunction(sqlConn, row):
        data = {columnNames[i] : row[i] for i in range(len(columnNames))}
        
        for columnName in columnNames:
            if data[columnName] == None:
                rowType = sqlConn.getColumnType(accessTableName, columnName)
                if rowType in ('int', 'float', 'decimal'):
                    data[columnName] = 0
                elif rowType in ('nvarchar', 'varchar', 'ntext', 'text'):
                    data[columnName] = ''
                # elif rowType == 'datetime2':
                #     dataValue = datetime(1970, 1, 1, 0, 0, 0, 0)
            try:
                data[columnName] = data[columnName].strip().lower()
            except:
                pass
        sqlConn.insertRow(accessTableName, data, allowNulls=False)
    
    return conversionFunction