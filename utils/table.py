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


    def create(self, tableFields):
        try:
            createSql = f"CREATE TABLE [{self.tableName}] ({tableFields})"
            self.sqlCursor.execute(createSql)
        except:
           self.handleError()

    def commit(self):
        try:
          self.sqlConn.commit()
        except:
           self.handleError()

    def handleError(self):
       print(f"There was an error in the {self.tableName} table.")
       if (self.currentProcess == ""):
          errorMessage = "    [Error initializing table object.]"
       elif (self.currentProcess == "droppingTable"):
          errorMessage = "    [Error dropping the table.]"
       elif (self.currentProcess == "creatingTable"):
          errorMessage = "    [Error dropping the table.]"
       elif (self.currentProcess == "droppingTable"):
          errorMessage = "    [Error dropping the table.]"