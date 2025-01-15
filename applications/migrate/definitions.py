from src.utils.conversionHelpers import getAccessDbName

from .conversionDefinitions.tablesToMigrate import tablesToMigrate as tablesToMigrateDefault

from src.types.Field import Field

def getMigrationDefinitions(connFactory, tablesToMigrate=tablesToMigrateDefault):
    definitionsConn = connFactory()
    sqlTableDefinitions = {
        tableName : 
            (
                getSqlTableFields(definitionsConn, tableName), 
                getSqlTableIndexes(definitionsConn, tableName), 
                getSqlTableForeignKeys(definitionsConn, tableName)
            ) for tableName in tablesToMigrate
    }
    accessConversionDefinitions = {
        tableName : getAccessConversionFunction(definitionsConn, tableName) for tableName in tablesToMigrate
    }
    definitionsConn.close()
    
    return sqlTableDefinitions, accessConversionDefinitions


def getSqlTableFields(conn, accessTableName):
    structureDetails = conn.accessGetTableStructure(getAccessDbName(accessTableName), accessTableName)
    fields = []
    for column in structureDetails['columnsInfo']:
        fields.append(Field(column['name'], column['details']))
        
    return fields

def getSqlTableIndexes(conn, accessTableName):
    return []

def getSqlTableForeignKeys(conn, accessTableName):
    return []

def getAccessConversionFunction(conn, accessTableName):
    columnNames = [column['name'] for column in conn.accessGetTableStructure(getAccessDbName(accessTableName), accessTableName)['columnsInfo']]

    def conversionFunction(conversionConn, row):
        data = {columnNames[i] : row[i] for i in range(len(columnNames))}
        
        for columnName in columnNames:
            if data[columnName] == None:
                rowType = conversionConn.sqlGetColumnType(accessTableName, columnName)
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
        conversionConn.sqlInsertRow(accessTableName, data, allowNulls=False)
    
    return conversionFunction