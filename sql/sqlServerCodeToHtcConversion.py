import os

from typing import List

def snake_to_camel(snake_str):
    """Converts a snake_case string to camelCase."""
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def convertSqlToPython(convertTables : List[str]):
    tables = {}
    script_dir = os.path.dirname(__file__)
    with open(os.path.join(script_dir, 'HTC.sql'), "r") as file:
        content = file.read()

        for sqlCommand in content.split("GO"):
            sql = sqlCommand.strip()
            if sql[0:12] == "CREATE TABLE":
                tableNameStart = sql.find("[") + 1
                tableNameEnd = sql.find("]")
                tableName = sql[tableNameStart:tableNameEnd]

                fieldDefinitionStart = sql.find("(") + 1
                fieldDefinitionEnd = sql.rfind(")")
                fieldDefinitionsArr = sql[fieldDefinitionStart:fieldDefinitionEnd].strip().split('\n')
                fieldDefinitions = {}
                for definition in fieldDefinitionsArr:
                    fieldNameStart = definition.find("[") + 1
                    fieldNameEnd = definition.find("]")
                    fieldName = definition[fieldNameStart:fieldNameEnd]
                    fieldDetails = definition[fieldNameEnd + 2:]
                    fieldDefinitions[fieldName] = fieldDetails
                    
                tableDetails = {
                    'fieldDefinitions' : fieldDefinitions
                }
                
                tables[tableName] = tableDetails
            
            elif sql[0:11] == "ALTER TABLE":
                tableNameStart = sql.find("[") + 1
                tableNameEnd = sql.find("]")
                tableName = sql[tableNameStart:tableNameEnd]
                
                foreignKeyDefinitions = {}
                
                foreignKeyIndex = sql.find('FOREIGN KEY')
                foreignKeyFieldNameStart = sql[foreignKeyIndex:].find('[') + 1 + foreignKeyIndex
                foreignKeyFieldNameEnd = sql[foreignKeyIndex:].find(']') + foreignKeyIndex
                foreignKeyFieldName = sql[foreignKeyFieldNameStart:foreignKeyFieldNameEnd]
                
                foreignKeyDefinitions['fromFieldName'] = foreignKeyFieldName
                
                referencesIndex = sql.find('REFERENCES')
                foreignKeyTableNameStart = sql[referencesIndex:].find('[') + 1 + referencesIndex
                foreignKeyTableNameEnd = sql[referencesIndex:].find(']') + referencesIndex
                foreignKeyTableName = sql[foreignKeyTableNameStart:foreignKeyTableNameEnd]
                
                foreignKeyDefinitions['toTableName'] = foreignKeyTableName
                
                foreignKeyForeignFieldNameStart = sql[referencesIndex:].find('(') + 2 + referencesIndex
                foreignKeyForeignFieldNameEnd = sql[referencesIndex:].find(')') - 1 + referencesIndex
                foreignKeyForeignFieldName = sql[foreignKeyForeignFieldNameStart:foreignKeyForeignFieldNameEnd]
                
                foreignKeyDefinitions['toFieldName'] = foreignKeyForeignFieldName
                
                if not 'foreignKeyDefinitions' in  tables[tableName]: 
                    tables[tableName]['foreignKeyDefinitions'] = [foreignKeyDefinitions]
                else:
                    tables[tableName]['foreignKeyDefinitions'].append(foreignKeyDefinitions)
                    
            elif sql[0:1] == 'INDEX':
                indexDefinitions = {}
                
                if not 'foreignKeyDefinitions' in  tables[tableName]: 
                    tables[tableName]['foreignKeyDefinitions'] = [foreignKeyDefinitions]
                else:
                    tables[tableName]['foreignKeyDefinitions'].append(foreignKeyDefinitions)
    
    for tableName, tableDetails in tables.items():
        if tableName in convertTables:
            varTableName = snake_to_camel(tableName)
            currTableFilePath = os.path.join(script_dir, rf'..\src\tables\sql\{tableName}.py')
            if os.path.exists(currTableFilePath):
                os.remove(currTableFilePath)
            with open(currTableFilePath, 'w+') as f:
                f.write('from ...imports import *\n')
                f.write('\n')
                f.write(f'{varTableName}Fields: List[Field] = [\n')
                for fieldName, fieldDetails in tableDetails['fieldDefinitions'].items():
                    f.write(f'    Field(fieldName="{fieldName}", fieldDetails="{fieldDetails[:-1] if fieldDetails[-1] == ',' else fieldDetails}"),\n')
                f.write(']\n')
                f.write('\n')
                f.write(f'{varTableName}Indexes: List[Index] = [\n')
                if 'indexDefinition' in tableDetails:
                    for indexDefinition in tableDetails['indexDefinitions']:
                        f.write(f"    Index('{tableName}', '{foreignKeyDefinition["toTableName"]}', '{foreignKeyDefinition["toFieldName"]}'),\n")
                f.write(']\n')
                f.write('\n')
                f.write(f'{varTableName}ForeignKeys: List[ForeignKey] = [\n')
                if 'foreignKeyDefinitions' in tableDetails:
                    for foreignKeyDefinition in tableDetails['foreignKeyDefinitions']:
                        f.write(f"    ForeignKey('{tableName}', '{foreignKeyDefinition["fromFieldName"]}', '{foreignKeyDefinition["toTableName"]}', '{foreignKeyDefinition["toFieldName"]}'),\n")
                f.write(']\n')
                f.write('\n')
                f.write(f"def create{varTableName[0].upper() + varTableName[1:]}Table(conn):\n")
                f.write(f"    {varTableName}Table = SqlTable('{tableName}', conn, {varTableName}Fields, {varTableName}Indexes, {varTableName}ForeignKeys)\n")
                f.write(f"    {varTableName}Table.createTable()\n")
                f.write(f"    {varTableName}Table.addIndexes()\n")
                f.write(f"\n")
                f.write(f"    return {varTableName}Table\n")
                f.write(f"\n")
                f.write(f"def add{varTableName[0].upper() + varTableName[1:]}(\n")
                f.write(f"    conn : Connection,\n")
                for fieldName, fieldDetails in tableDetails['fieldDefinitions'].items():
                    if (fieldName == 'id'):
                        continue
                    fieldSqlType = fieldDetails.split(' ')[0]
                    if fieldSqlType[0:8] == 'NVARCHAR' or fieldSqlType[0:7] == 'VARCHAR' or fieldSqlType[0:9] == 'DATETIME2':
                        fieldType = 'str'
                    elif fieldSqlType[0:7] == 'INTEGER':
                        fieldType = 'int'
                    elif fieldSqlType[0:3] == 'BIT':
                        fieldType = 'bool'
                    elif fieldSqlType[0:7] == 'DECIMAL' or fieldSqlType[0:5] == 'MONEY':
                        fieldType = 'float'
                        
                    f.write(f"    {snake_to_camel(fieldName)} : {fieldType},\n")
                f.write(f") -> int:\n")
                whereClauses = []
                for fieldName in tableDetails['fieldDefinitions']:
                    if (fieldName == 'id'):
                        continue
                    whereClauses.append(f"[{fieldName}] = '{"{" + snake_to_camel(fieldName) + "}"}'")
                whereClause = 'f"' + ' AND '.join(whereClauses) + '"'
                f.write(f"    {varTableName}Row = conn.sqlGetInfo('{tableName}', 'id', {whereClause})\n")
                f.write(f"    if {varTableName}Row:\n")
                f.write(f"        return {varTableName}Row[0].id\n")
                f.write(f"    data = {'{'}\n")
                for fieldName in tableDetails['fieldDefinitions']:
                    if (fieldName == 'id'):
                        continue
                    f.write(f"        '{fieldName}' : {snake_to_camel(fieldName)},\n")
                f.write(f"    {'}'}\n")
                f.write(f"    conn.sqlInsertRow('{tableName}', data)\n")
                f.write(f"    conn.commit()\n")
                f.write(f"\n")
                f.write(f"    return conn.sqlGetLastIdCreated('{tableName}')")
                
                
convertSqlToPython([
    'aci_data',
    'aci_data_change_history',
    'address_change_history',
    'agent',
    'agent_change_history',
    'agent_certification_test',
    'archive_history',
    'archive_error_log',
    'assessorial',
    'assessorial_change_history',
    'branch',
    'branch_change_history',
    'certification_test',
    'certification_test_change_history',
    'certification_test_trainer',
    'certification_test_trainer_change_history',
    'company_change_history',
    'customer',
    'customer_change_history',
    'customer_default_assessorial',
    'holiday',
    'location',
    'location_change_history',
    'location_default_assessorial',
    'overnight_maintenance_history',
    'order',
    'order_change_history',
    'order_assessorial',
    'order_attachment',
    'order_dim',
    'order_driver',
    'order_status',
    'order_status_change_history',
    'order_type',
    'position_change_history',
    'rate',
    'rate_area',
    'rate_change_history',
    'special',
    'special_change_history',
    'user_change_history',
])