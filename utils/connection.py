from typing import Dict, Any, List, Optional
from pyodbc import Connection, Cursor

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

  def sqlDrop(self, tableName : str) -> None:
    self.currentProcess = "droppingSqlTable"
    try:
      dropSql: str = f"DROP TABLE IF EXISTS [{tableName}]"
      self.sqlCursor.execute(dropSql)
    except Exception as err:
      self.handleError(str(err))

  def sqlCreateTable(self, tableName: str, tableFields: str) -> None:
    self.currentProcess = "creatingSqlTable"
    try:
      self.sqlDrop(tableName=tableName)
      createSql: str = f"CREATE TABLE [{tableName}] ({tableFields})"
      self.sqlCursor.execute(createSql)
    except Exception as err:
      self.handleError(str(err))

  def sqlInsertRow(self, tableName : str, fields: Dict[str, Any]) -> None:
    self.currentProcess = "insertingSqlRow"
    try:
      fieldNames: List[str] = list(fields.keys())
      fieldNamesString: str = ', '.join(f'[{name}]' for name in fieldNames)
      placeholders: str = ', '.join(['?'] * len(fields))
      fieldValues: List[Any] = list(fields.values())
      
      insertSql: str = f"INSERT INTO [{self.tableName}] ({fieldNamesString}) VALUES ({placeholders})"
      self.sqlCursor.execute(insertSql, fieldValues)
    except Exception as err:
      self.handleError(str(err), info={'tableName' : tableName, 'fields': fields})
      
  def sqlAddForeignKey(self, fromTableName: str, fromTableField: str, toTableName: str, toTableField: str) -> None:
    self.currentProcess = "addingForeignKey"
    try:
      addForeignKeySql: str = f"ALTER TABLE [{fromTableName}] ADD FOREIGN KEY ([{fromTableField}]) REFERENCES [{toTableName}] ([{toTableField}])"
      self.sqlCursor.execute(addForeignKeySql)
    except Exception as err:
      self.handleError(
        info={
          "fromTableName": fromTableName, 
          'fromTableField': fromTableField,
          'toTableName': toTableName,
          "toTableField": toTableField
        }
      )
      
  def sqlAddIndex(self, tableName : str, indexType: str, indexField: str, indexName: str, isUnique: bool = False) -> None:
    self.currentProcess = "addingSqlIndex"
    try:
      validIndexTypes: List[str] = ["clustered", "nonclustered"]
      if indexType not in validIndexTypes:
        raise Exception(f"Index not of valid type ({validIndexTypes}).")
      uniqueClause: str = "UNIQUE " if isUnique else ""
      addIndexSql: str = f"CREATE {uniqueClause}{indexType.upper()} INDEX [{indexName}] ON [{tableName}] ([{indexField}])"
      self.sqlCursor.execute(addIndexSql)
    except Exception as err:
      self.handleError(
        info={
          "tableName" : tableName,
          "indexType": indexType, 
          "indexField": indexField, 
          "indexName": indexName, 
          "isUnique": isUnique
        }
      )
      
  def accessGetTableInfo(
    self, 
    accessDb: str,
    tableName: str,
    selectRows: Optional[List[str]] = None,
    whereClause: str = ""
  ) -> List[Any]:
    self.currentProcess = 'gettingAccessTableInfo'
    try:
      accessConn: Connection = self.dbConnections[accessDb]
      accessCursor: Cursor = accessConn.cursor()
      if selectRows:
        selectColumns: str = ', '.join(selectRows)
      else:
        selectColumns: str = '*'
      selectSql: str = f"SELECT {selectColumns} FROM [{tableName}] {f'WHERE {whereClause}' if whereClause else ''}"
      accessCursor.execute(selectSql)
      rows: List[Any] = accessCursor.fetchall()
      return rows
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
      
  def accessCheckIfValueExistsInColumn(self, tableName, fieldName: str, fieldValue: Any) -> bool:
    self.currentProcess = 'checkingIfValueExistsInColumn'
    try:
      checkSql: str = f"SELECT COUNT(1) FROM [{tableName}] WHERE [{fieldName}] = ?"
      self.sqlCursor.execute(checkSql, (fieldValue,))
      result = self.sqlCursor.fetchone()
      if result and result[0] > 0:
        return True
      else:
        return False
    except Exception as err:
      self.handleError(
        info={
          'tableName': tableName,
          'fieldName': fieldName,
          'fieldValue': fieldValue,
          'valueType': type(fieldValue)
        }
      )
      return False

  def handleError(self, info: Optional[Dict[str, Any]] = None) -> None:
    if self.currentProcess == '':
      errorMessage: str = '    Error initializing connection object.'
    elif self.currentProcess == 'droppingSqlTable':
      errorMessage = f'    Error dropping table [{info['tableName']}].'
    elif self.currentProcess == 'creatingTable':
      errorMessage = f'    Error creating table [{info['tableName']}].'
    elif self.currentProcess == 'insertingRow':
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
    elif self.currentProcess == "gettingAccessTable":
      errorMessage = "    [Error getting access table data.]"
    elif self.currentProcess == "checkingIfValueExistsInColumn":
      errorMessage = "    [Error checking if value exists in column.]"
    elif self.currentProcess == "committing":
      errorMessage = "    [Error committing statement.]"
    else:
      errorMessage = "Error message not defined"
      
    print(errorMessage)
    print("Detailed Error Message:")
    print(traceback.format_exc())
