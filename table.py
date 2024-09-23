class Table():
    def __init__(self, sqlCursor):
        self.sqlCursor = sqlCursor
        
    def createTable(self, createTableString):
        self.sqlCursor.execute()