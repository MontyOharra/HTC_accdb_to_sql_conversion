from typing import Dict, Any, List

from pyodbc import Cursor

class Table():
   def __init__(self, tableName : str, dbConnections : Dict[str, Cursor]):
        if ("sqlServer" in list(dbConnections.keys())):
          sqlConn = dbConnections["sqlServer"]
         
        self.dbConnections = dbConnections
        self.tableName = tableName
        self.sqlConn = sqlConn
        self.sqlCursor = sqlConn.cursor()
        self.currentProcess = ""

   def drop(self):
        self.currentProcess = "droppingTable"
        try:
          dropSql = f"DROP TABLE IF EXISTS [{self.tableName}]"
          self.sqlCursor.execute(dropSql)
        except Exception as err:
           self.handleError(str(err))

   def createTable(self, tableFields):
        self.currentProcess = "creatingTable"
        try:
            self.drop()
            createSql = f"CREATE TABLE [{self.tableName}] ({tableFields})"
            self.sqlCursor.execute(createSql)
        except Exception as err:
           self.handleError(str(err))

   def insertRow(self, fields : Dict[str, Any]):
        self.currentProcess = "insertingRow"
        try:
            fieldNames = list(fields.keys())
            fieldNamesString = ', '.join(fieldNames)
            
            fieldValues = list(fields.values())
            fieldValuesString = ', '.join([f"\'{value}\'" if isinstance(value, str) else f"{value}" for value in fieldValues])
            insertSql = f"INSERT INTO [{self.tableName}] ({fieldNamesString}) VALUES ({fieldValuesString})"
            self.sqlCursor.execute(insertSql)
        except Exception as err:
           self.handleError(str(err), info=fields)
            
   def addForeignKey(self, thisTableField, foreignTableName, foreignTableField):
      self.currentProcess = "addingForeignKey"
      
      try:
         addForeignKeySql = f"ALTER TABLE [{self.tableName}] ADD FOREIGN KEY ([{thisTableField}]) REFERENCES [{foreignTableName}] ([{foreignTableField}])"
         self.sqlCursor.execute(addForeignKeySql)
      except Exception as err:
         self.handleError(
            str(err), 
            info = {
               "tableName": foreignTableName, 
               "tableField": foreignTableField
            }
         )
         
   def addIndex(self, indexType, indexField, indexName, isUnique=False):
      self.currentProcess = "addingIndex"
      try:
         validIndexTypes = ["clustered", "nonclustered"]
         if indexType not in validIndexTypes:
            raise Exception(f"Index not of valid type ({validIndexTypes}).")
         addIndexSql = f"CREATE{' UNIQUE ' if isUnique else ' '} {indexType} INDEX {indexName} ON [{self.tableName}] ({indexField})"
         self.sqlCursor.execute(addIndexSql)
      except Exception as err:
         self.handleError(
            str(err), 
            info = {
               "indexType": indexType, 
               "indexField": indexField, 
               "indexName": indexName, 
               "isUnique": isUnique
            }
         )
         
   def getAccessTable(self, 
      accessDb : str,
      accessTableName : str,
      selectRows : List[str] = [],
      whereClause : str = "",
      
   ):
      self.currentProcess = 'gettingAccessTable'
      try:
        accessConn = self.dbConnections[accessDb]
        accessCursor = accessConn.cursor()
        selectSql = f'SELECT {"*" if not selectRows else f"{', '.join(selectRows)}"} FROM [{accessTableName}] {f"WHERE {whereClause}" if whereClause else ""}'
        accessCursor.execute(selectSql)
        rows = accessCursor.fetchall()
        return rows
      except Exception as err:
        self.handleError(str(err))
         
         
   def commit(self):
        self.currentProcess = "committing"
        try:
          self.sqlConn.commit()
        except Exception as err:
           self.handleError(str(err))
           

   def handleError(self, errorDetail, info = None):
     
      if (self.currentProcess == ""):
         errorMessage = "    [Error initializing table object.]"
      elif (self.currentProcess == "droppingTable"):
         errorMessage = "    [Error dropping the table.]"
      elif (self.currentProcess == "creatingTable"):
         errorMessage = "    [Error creating the table.]"
      elif (self.currentProcess == "insertingRow"):
         errorMessage = "    [Error inserting row.] Details:"
         errorMessage += "\n"
         for fieldName, fieldValue in info.items():
            errorMessage += f"        Name: [{fieldName}], Value: [{fieldValue}], Type: [{type(fieldValue)}]"
      elif (self.currentProcess == "addingIndex"):
         errorMessage = "    [Error adding index.] Details:"
         errorMessage += "\n"
         errorMessage += f"        Column Name: [{info["indexField"]}], Index Type: '{info["indexType"]}{'and UNIQUE' if info["isUnique"] else ''}"
      elif (self.currentProcess == "committing"):
         errorMessage = "    [Error committing statement.]"
      elif (self.currentProcess == "addingForeignKey"):
         errorMessage = "    [Error adding foreign key.] Details:"
      elif (self.currentProcess == "gettingAccessTable"):
         errorMessage = "    [Error getting access table data.]"
      else:
         errorMessage = "Error message not defined"
            
      print(f"There was an error in the {self.tableName} table:")
      print(errorMessage)
      print(f"Detailed Error Message:")
      print(errorDetail)
