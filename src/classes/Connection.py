from typing import Dict, Any, List, Optional
from pyodbc import Connection, Cursor

from ..types.Field import Field
from ..types.ForeignKey import ForeignKey
from ..types.Index import Index

import traceback

class Connection:
  def __init__(self, dbConnections: Dict[str, Connection]):
    if "sqlServer" in dbConnections:
      sqlConn: Connection = dbConnections["sqlServer"]
    else:
      raise Exception("SQL Server connection not found in dbConnections.")
    
    self.dbConnections: Dict[str, Connection] = dbConnections
    self.sqlConn: Connection = sqlConn
    self.sqlCursor: Cursor = sqlConn.cursor()
    self.currentProcess: str = ""

  def sqlDropTable(self, tableName : str) -> None:
    self.currentProcess = "droppingSqlTable"
    dropSql: str = f"DROP TABLE IF EXISTS [{tableName}]"
    try:
      self.sqlCursor.execute(dropSql)
      self.commit()
    except Exception as err:
      self.handleError(
        info={
          'sqlStatement' : dropSql,
          'tableName' : tableName
        }
      )

  def sqlCreateTable(self, tableName: str, tableFields: List[Field]) -> None:
    self.currentProcess = "creatingSqlTable"
    tableFieldsString = ', '.join([f'[{field.fieldName}] {field.fieldDetails}' for field in tableFields])
    createSql: str = f"CREATE TABLE [{tableName}] ({tableFieldsString})"
    try:
      self.sqlDropTable(tableName)
      self.sqlCursor.execute(createSql)
      self.commit()
    except Exception as err:
      self.handleError(
        info={
          'sqlStatement' : createSql,
          'tableName' : tableName
        }
      )

  def sqlInsertRow(self, tableName : str, fields: Dict[str, Any]) -> None:
    self.currentProcess = "insertingSqlRow"
    fieldNames: List[str] = list(fields.keys())
    fieldValues: List[Any] = []
    for value in fields.values():
      if type(value) == str:
        if value.strip() == "":
          fieldValues.append("NULL")
        else:
          fieldValues.append(f"'{''.join(["''" if x == "'" else x for x in value])}'".strip())
      elif type(value) == int or type(value) == float:
        fieldValues.append(value)
      elif type(value) == bool:
        if value == True:
          fieldValues.append('1')
        else:
          fieldValues.append('0')
      elif value == None:
        fieldValues.append('NULL')
      else:
        fieldValues.append(f"'{value}'")
    fieldNamesString: str = ', '.join(f'[{name}]' for name in fieldNames)
    insertValuesString: str = ', '.join(f"{value}" for value in fieldValues)
    
      
    insertSql: str = f"INSERT INTO [{tableName}] ({fieldNamesString}) VALUES ({insertValuesString})"
    try:
      self.sqlCursor.execute(insertSql)
      self.commit()
    except Exception as err:
      self.handleError(
        info={
          'sqlStatement' : insertSql,
          'tableName' : tableName,
          'fields': fields,
        }
      )
      
  def sqlAddForeignKey(self, fromTableName: str, fromTableField: str, toTableName: str, toTableField: str) -> None:
    self.currentProcess = "addingSqlForeignKey"
    addForeignKeySql: str = f"ALTER TABLE [{fromTableName}] ADD FOREIGN KEY ([{fromTableField}]) REFERENCES [{toTableName}] ([{toTableField}])"
    try:
      self.sqlCursor.execute(addForeignKeySql)
      self.commit()
    except Exception as err:
      self.handleError(
        info={
          'sqlStatement' : addForeignKeySql,
          'fromTableName': fromTableName, 
          'fromTableField': fromTableField,
          'toTableName': toTableName,
          'toTableField': toTableField
        }
      )
      
  def sqlAddIndex(self, tableName : str, indexType: str, indexFields: str | List[str], indexName: str, isUnique: bool = False) -> None:
    self.currentProcess = "addingSqlIndex"
    validIndexTypes: List[str] = ["clustered", "nonclustered"]
    if indexType not in validIndexTypes:
      raise Exception(f"Index not of valid type ({validIndexTypes}).")
    uniqueClause: str = "UNIQUE " if isUnique else ""
    if type(indexFields) == str:
      indexFieldClause = f'[indexFields]'
    elif type(indexFields) == List:
      indexFieldClause = ', '.join(f'[{indexField}]' for indexField in indexFields)
    addIndexSql: str = f"CREATE {uniqueClause}{indexType.upper()} INDEX [{indexName}] ON [{tableName}] ({indexFieldClause})"
    try:
      self.sqlCursor.execute(addIndexSql)
      self.commit()
    except Exception as err:
      self.handleError(
        info={
          'sqlStatement' : addIndexSql,
          'tableName' : tableName,
          'indexType': indexType, 
          'indexFields': indexFields, 
          'indexName': indexName, 
          'isUnique': isUnique
        }
      )
      
  def sqlGetInfo(
    self,
    tableName: str,
    selectDetails : List[str | Dict[str, str]] | str | None = None,
    whereDetails : Dict[str, any] | str | None = None
  ) -> List[Any]:
    self.currentProcess = 'gettingSqlInfo'
    
    # Create column selection string
    selectColumnsClause : str
    if type(selectDetails) ==  list: # Columns can be a single string, or a dictionary, with the key being the column name and value being its alias
      selectColumnsClause = ', '.join([column if type(column) == str else f"{list(column.keys())[0]} AS {list(column.values())[0]}" for column in selectDetails])
    elif type(selectDetails) == str: # If column is single string
      selectColumnsClause = selectDetails
    else: # Otherwise select all columns
      selectColumnsClause = '*'
    
    # Create where clause
    if type(whereDetails) == dict:  
      whereArgs = []
      for tableField, fieldValue in whereDetails.items():
        if fieldValue == None: # If value is None, check if NULL in SQL
          whereArgs.append(f"[{tableField}] IS NULL")
        elif type(fieldValue) == str: # If string type, double up any single quotations within the string for escaping
          fieldValue = ''.join(["''" if x == "'" else x for x in fieldValue])
          whereArgs.append(f"[{tableField}] LIKE '{fieldValue}'")
        elif type(fieldValue) == int or type(fieldValue) == float: # IF numeric type, do not include quotations
          whereArgs.append(f"[{tableField}] = {fieldValue}")
        elif type(fieldValue) == bool: # If boolean type, convert to 1/0 instead of true/false
          if fieldValue == True:
            whereArgs.append(f"[{tableField}] = 1")
          else:
            whereArgs.append(f"[{tableField}] = 0")
        else: # In all unchecked cases, check equality with single quotations around value
          whereArgs.append(f"[{tableField}] = '{fieldValue}'")
        whereClause = ' AND '.join(whereArgs)
        
    elif type(whereDetails) == str:
      whereClause = whereDetails
    else:
      whereClause = ''

    selectSql: str = f"SELECT {selectColumnsClause} FROM {f'[{tableName}]' if len(tableName.split(' ')) == 1 else tableName} {f'WHERE {whereClause}' if whereClause else ''}"
    try:
      self.sqlCursor.execute(selectSql)
      return self.sqlCursor.fetchall()
    except Exception as err:
      self.handleError(
        info={
          'sqlStatement' : selectSql,
          'tableName' : tableName,
          'whereDetails': whereDetails,
        }
      )
   
  def sqlGetLastIdCreated(self, tableName : str) -> int:
    self.currentProcess = 'gettingSqlLastIdCreated'
    selectSql = f"SELECT IDENT_CURRENT('{tableName}') AS current_id"
    try:
      self.sqlCursor.execute(selectSql)
      rows = self.sqlCursor.fetchall()
      return rows[0].current_id
    except Exception as err:
      self.handleError(
        info={
          'sqlStatement' : selectSql,
          'tableName': tableName
        }
      )
           
  def accessGetTableInfo(
    self, 
    accessDb: str,
    tableName: str,
    selectColumns: Optional[List[str]] = None,
    whereClause: str = ""
  ) -> List[Any]:
    self.currentProcess = 'gettingAccessInfo'
    if selectColumns:
      selectColumns: str = ', '.join(selectColumns)
    else:
      selectColumns: str = '*'
    selectSql: str = f"SELECT {selectColumns} FROM [{tableName}] {f'WHERE {whereClause}' if whereClause else ''}"
    try:
      accessConn: Connection = self.dbConnections[accessDb]
      accessCursor: Cursor = accessConn.cursor()
      accessCursor.execute(selectSql)
      return accessCursor.fetchall()
    except Exception as err:
      self.handleError(
        info={
          'sqlStatement' : selectSql,
          'accessDb': accessDb,
          'tableName' : tableName,
          'selectColumns' : selectColumns,
          'whereClause' : whereClause
        }
      )
      
  def commit(self) -> None:
    self.currentProcess = 'committing'
    try:
      self.sqlConn.commit()
    except Exception as err:
      self.handleError(str(err))      

  def handleError(self, info: Optional[Dict[str, Any]] = None) -> None:
    if self.currentProcess == '':
      errorMessage: str = 'Error initializing connection object.\n'
    elif self.currentProcess == 'droppingSqlTable':
      errorMessage = f'Error dropping table [{info['tableName']}].\n'
    elif self.currentProcess == 'creatingSqlTable':
      errorMessage = f'Error creating table [{info['tableName']}].\n'
    elif self.currentProcess == 'insertingSqlRow':
      errorMessage = f'Error inserting row into [{info['tableName']}].\n    Details:\n'
      for fieldName, fieldValue in info['fields'].items():
        errorMessage += f'        Name: [{fieldName}], Value: [{fieldValue}], Type: [{type(fieldValue)}]\n'
    elif self.currentProcess == "addingIndex":
      errorMessage = f"Error adding index onto [{info['tableName']}].\n    Details:\n"
      errorMessage += f"        Column Name: [{info['indexField']}], Index Type: '{info['indexType']}', Is Unique: {info['isUnique']}"
    elif self.currentProcess == "addingSqlForeignKey":
      errorMessage = f"Error adding foreign key to [{info['fromTableName']}].\n    Details:\n"
      errorMessage += f'            From field: [{info['fromTableField']}], Target table: [{info['toTableName']}], Target table field: [{info['toTableField']}]'
    elif self.currentProcess == f"gettingSqlInfo":
      errorMessage = f'Error getting info from [{info['tableName']}].\n    Details:\n'
      for fieldName, fieldValue in info['whereDetails'].items():
        errorMessage += f'        Name: [{fieldName}], Value: [{fieldValue}], Type: [{type(fieldValue)}]\n'
    elif self.currentProcess == 'gettingSqlLastIdCreated':
      errorMessage = f'Error getting last id created in [{info['tableName']}].\n'
    elif self.currentProcess == "gettingAccessTable":
      errorMessage = "Error getting access table data.\n"
    elif self.currentProcess == "committing":
      errorMessage = "Error committing statement.\n"
    else:
      errorMessage = "Error message not defined\n"
      
    errorMessage += f'\n    SQL:\n        {info['sqlStatement']}'
    print(errorMessage)
    print("    Detailed Error Message:")
    print(f'        {''.join([char if char != "\n" else '\n        ' for char in traceback.format_exc()])}')
    print('\n')
