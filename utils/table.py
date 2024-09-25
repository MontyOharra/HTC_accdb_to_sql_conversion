class Table():
    def __init__(self, tableName, sqlConn):
        self.tableName = tableName
        self.sqlConn = sqlConn
        self.sqlCursor = sqlConn.cursor()

    def drop(self):
        try:
          dropSql = f"DROP TABLE IF EXISTS [{self.tableName}]"
          self.sqlCursor.execute(dropSql)
        except:
          print()

    def create(self, tableFields):
        createSql = f"CREATE TABLE [{self.tableName}] ({tableFields})"
        self.sqlCursor.execute(createSql)

    def commit(self):
        self.sqlConn.commit()