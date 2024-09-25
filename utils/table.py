from typing import Dict, Any

class Table():
   def __init__(self, tableName, sqlConn):
        self.tableName = tableName
        self.sqlConn = sqlConn
        self.sqlCursor = sqlConn.cursor()

        self.currentProcess = ""

   def drop(self):
        try:
          self.currentProccess = "droppingTable"
          dropSql = f"DROP TABLE IF EXISTS [{self.tableName}]"
          self.sqlCursor.execute(dropSql)
        except:
           self.handleError()

   def createTable(self, tableFields):
        try:
            self.currentProccess = "creatingTable"
            createSql = f"CREATE TABLE [{self.tableName}] ({tableFields})"
            self.sqlCursor.execute(createSql)
        except:
           self.handleError()

   def addRow(self, fields : Dict[str, Any]):
        try:   
            self.currentProccess = "insertingRow"
            fieldNames = list(fields.keys())
            fieldNamesString = ', '.join(fieldNames).rstrip(', ')
            
            fieldValues = list(fields.items())
            fieldValuesString = ', '.join(fieldValues).rstrip(', ')
            insertSql = f"INSERT INTO [{self.tableName}] ({fieldNamesString}) VALUES ({fieldValuesString})"
            
            self.sqlCursor.execute(insertSql)
        except:
           self.handleError(fields)
           
   def addForeignKey(self, thisTableField, foreignTableName, foreignTableField):
      try:
         self.currentProccess = "addingForeignKey"
         addForeignKeySql = f"ALTER TABLE [{self.tableName}] ADD FOREIGN KEY ([{thisTableField}]) REFERENCES [{foreignTableName}] ([{foreignTableField}])"
         self.sqlCursor.execute(addForeignKeySql)
      except Exception as err:
         self.handleError([foreignTableName, foreignTableField])
         
        

   def commit(self):
        try:
          self.sqlConn.commit()
        except:
           self.handleError()
           

   def handleError(self, errorDetail, info = None):
      if (self.currentProcess == ""):
         errorMessage = "    [Error initializing table object.]"
      elif (self.currentProcess == "droppingTable"):
         errorMessage = "    [Error dropping the table.]"
      elif (self.currentProcess == "creatingTable"):
         errorMessage = "    [Error dropping the table.]"
      elif (self.currentProcess == "insertingRow"):
         errorMessage = "    [Error inserting row.] Details:"
         errorMessage += "\n"
         for fieldName, fieldValue in info.items():
            errorMessage += f"        Name: [{fieldName}], Value: [{fieldValue}], Type: [{type(fieldValue)}]"
            
      print(f"There was an error in the {self.tableName} table:\n")
      print(errorMessage)