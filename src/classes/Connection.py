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
    try:
      dropSql: str = f"DROP TABLE IF EXISTS [{tableName}]"
      self.sqlCursor.execute(dropSql)
      self.commit()
    except Exception as err:
      self.handleError(
        info={
          'tableName' : tableName
        }
      )

  def sqlCreateTable(self, tableName: str, tableFields: List[Field]) -> None:
    self.currentProcess = "creatingSqlTable"
    try:
      self.sqlDropTable(tableName)
      tableFieldsString = ', '.join([f'[{field.fieldName}] {field.fieldDetails}' for field in tableFields])
      createSql: str = f"CREATE TABLE [{tableName}] ({tableFieldsString})"
      self.sqlCursor.execute(createSql)
      self.commit()
    except Exception as err:
      self.handleError(
        info={
          'tableName' : tableName
        }
      )

  def sqlInsertRow(self, tableName : str, fields: Dict[str, Any]) -> None:
    self.currentProcess = "insertingSqlRow"
    try:
      fieldNames: List[str] = list(fields.keys())
      fieldNamesString: str = ', '.join(f'[{name}]' for name in fieldNames)
      placeholders: str = ', '.join(['?'] * len(fields))
      fieldValues: List[Any] = list(fields.values())
      
      insertSql: str = f"INSERT INTO [{tableName}] ({fieldNamesString}) VALUES ({placeholders})"
      self.sqlCursor.execute(insertSql, fieldValues)
      self.commit()
    except Exception as err:
      self.handleError(
        info={
          'tableName' : tableName,
          'fields': fields
        }
      )
      
  def sqlAddForeignKey(self, fromTableName: str, fromTableField: str, toTableName: str, toTableField: str) -> None:
    self.currentProcess = "addingSqlForeignKey"
    try:
      addForeignKeySql: str = f"ALTER TABLE [{fromTableName}] ADD FOREIGN KEY ([{fromTableField}]) REFERENCES [{toTableName}] ([{toTableField}])"
      self.sqlCursor.execute(addForeignKeySql)
      self.commit()
    except Exception as err:
      self.handleError(
        info={
          "fromTableName": fromTableName, 
          'fromTableField': fromTableField,
          'toTableName': toTableName,
          "toTableField": toTableField
        }
      )
      
  def sqlAddIndex(self, tableName : str, indexType: str, indexFields: str | List[str], indexName: str, isUnique: bool = False) -> None:
    self.currentProcess = "addingSqlIndex"
    try:
      validIndexTypes: List[str] = ["clustered", "nonclustered"]
      if indexType not in validIndexTypes:
        raise Exception(f"Index not of valid type ({validIndexTypes}).")
      uniqueClause: str = "UNIQUE " if isUnique else ""
      if type(indexFields) == str:
        indexFieldClause = f'[indexFields]'
      elif type(indexFields) == List:
        indexFieldClause = ', '.join(f'[{indexField}]' for indexField in indexFields)
      addIndexSql: str = f"CREATE {uniqueClause}{indexType.upper()} INDEX [{indexName}] ON [{tableName}] ({indexFieldClause})"
      self.sqlCursor.execute(addIndexSql)
      self.commit()
    except Exception as err:
      self.handleError(
        info={
          "tableName" : tableName,
          "indexType": indexType, 
          "indexFields": indexFields, 
          "indexName": indexName, 
          "isUnique": isUnique
        }
      )
      
  def sqlGetInfo(
    self,
    tableName: str,
    selectColumns: List[str] | str | None = None,
    whereDict : Dict[str, any] = None
  ) -> List[Any]:
    self.currentProcess = 'gettingSqlInfo'
    try:
      if type(selectColumns) ==  list:
        if selectColumns:
          selectColumns: str = ', '.join(selectColumns)
        else:
          selectColumns: str = '*'
      whereClause = ' AND '.join([f"{tableField} = {fieldValue}" for tableField, fieldValue in whereDict.items()])
      whereClause = ''.join(["''" if x == "'" else x for x in whereClause])
      selectSql: str = f"SELECT {selectColumns} FROM {f'[{tableName}]' if len(tableName.split(' ')) == 1 else tableName} {f'WHERE {whereClause}' if whereClause else ''}"
      self.sqlCursor.execute(selectSql)
      return self.sqlCursor.fetchall()
    except Exception as err:
      self.handleError(
        info={
          'tableName' : tableName,
          'selectRows' : selectColumns,
          'whereClause' : whereClause,
          'sqlStatement' : selectSql
        }
      )
   
  def sqlGetLastIdCreated(self, tableName : str) -> int:
    self.currentProcess = 'gettingSqlLastIdCreated'
    try:
      selectSql = f"SELECT IDENT_CURRENT('{tableName}') AS current_id"
      self.sqlCursor.execute(selectSql)
      rows = self.sqlCursor.fetchall()
      return rows[0].current_id
    except Exception as err:
      self.handleError(
        info={
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
    try:
      accessConn: Connection = self.dbConnections[accessDb]
      accessCursor: Cursor = accessConn.cursor()
      if selectColumns:
        selectColumns: str = ', '.join(selectColumns)
      else:
        selectColumns: str = '*'
      selectSql: str = f"SELECT {selectColumns} FROM [{tableName}] {f'WHERE {whereClause}' if whereClause else ''}"
      accessCursor.execute(selectSql)
      return accessCursor.fetchall()
    except Exception as err:
      self.handleError(
        info={
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
      errorMessage: str = '    Error initializing connection object.'
    elif self.currentProcess == 'droppingSqlTable':
      errorMessage = f'    Error dropping table [{info['tableName']}].'
    elif self.currentProcess == 'creatingSqlTable':
      errorMessage = f'    Error creating table [{info['tableName']}].'
    elif self.currentProcess == 'insertingSqlRow':
      errorMessage = f'    Error inserting row into [{info['tableName']}] Details:\n'
      for fieldName, fieldValue in info['fields'].items():
        errorMessage += f'        Name: [{fieldName}], Value: [{fieldValue}], Type: [{type(fieldValue)}]\n'
    elif self.currentProcess == "addingIndex":
      errorMessage = f"    Error adding index onto [{info['tableName']}]. Details:\n"
      errorMessage += f"        Column Name: [{info['indexField']}], Index Type: '{info['indexType']}'"
      if info['isUnique']:
        errorMessage += " and UNIQUE"
    elif self.currentProcess == "addingSqlForeignKey":
      errorMessage = f"    Error adding foreign key to [{info['tableName']}]. Details:\n"
      errorMessage += f'        From field: [{info['fromTableField']}], Target table: [{info['toTableName']}], Target table field: [{info['toTableField']}]'
    elif self.currentProcess == f"gettingSqlInfo":
      errorMessage = f'    Error getting info from [{info['tableName']}]. Details:\n'
      errorMessage = f'        SQL: {info['sqlStatement']}\n'
    elif self.currentProcess == 'gettingSqlLastIdCreated':
      errorMessage = f'    Error getting last id created in [{info['tableName']}].'
    elif self.currentProcess == "gettingAccessTable":
      errorMessage = "    Error getting access table data."
    elif self.currentProcess == "committing":
      errorMessage = "    Error committing statement."
    else:
      errorMessage = "Error message not defined"
      
    print(errorMessage)
    print("Detailed Error Message:")
    print(traceback.format_exc())
