from utils.connection import Connection

addressFields = '''
  [id] INTEGER PRIMARY KEY IDENTITY(1, 1),
  [address_line_1] NVARCHAR(255) NOT NULL,
  [address_line_2] NVARCHAR(50),
  [city_id] INTEGER NOT NULL,
  [postal_code_id] INTEGER NOT NULL,
  [region_id] INTEGER NOT NULL,
  [is_carrier] BIT NOT NULL DEFAULT (0),
  [is_local] BIT NOT NULL DEFAULT (0),
  [is_international] BIT NOT NULL DEFAULT (0)
'''

addressIndexes = {
  'ix_city': {
    'tableName': 'address',
    'indexType': 'nonclustered',
    'indexField': 'city_id'
  }
}

addressForeignKeys = [
  {
    'fromTableField': ''
  }
]

def createAddressTable(conn : Connection):
  conn.sqlCreateTable('address', addressFields)
  conn.commit()

def addAddressIndexes(conn : Connection):
  for indexName, details in addressIndexes.items():
    conn.sqlAddIndex(details['tableName'], details['indexType'], details['indexField'], indexName)

def addAddressForeignKeys(conn : Connection):
  for foreignKey in addressForeignKeys:
    conn.sqlAddForeignKey('address', foreignKey['fromTableField'], foreignKey['toTableName'], foreignKey['totableField'])

def insertAddressData():
  global addressTable
  branchInfo = addressTable.getAccessTable("htcAll", "branch")
  for row in branchInfo:
    print(row.country)
    
    addressTable.insertRow({
      'address_line_1' : row.address_line_1,
      'city_id': 1,
      'postal_code_id' : 1,
      'region_id' : 1,
      'is_carrier' : 1,
      'is_local': 0,
      'is_international': 0
      })

  addressTable.commit()