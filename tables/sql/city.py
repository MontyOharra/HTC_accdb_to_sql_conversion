from utils.connection import Connection

cityFields = '''
  [id] INTEGER UNIQUE PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [city_name] NVARCHAR NOT NULL,
  [lat] DECIMAL NOT NULL,
  [long] DECIMAL NOT NULL,
  [region_id] INTEGER NOT NULL
'''

cityIndexes = {
    
}

cityForeignKeys = [
    
]

def createCityTable(conn : Connection):
    conn.sqlCreateTable('city', cityFields)
    conn.commit()
    
def addCityIndexes(conn : Connection):
    for indexName, details in cityIndexes.items():
        conn.sqlAddIndex(details['tableName'], details['indexType'], details['indexField'], indexName)
        
