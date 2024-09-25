from utils.table import Table

tableFields = '''
  [id] INTEGER PRIMARY KEY IDENTITY(1, 1),
  [address_line_1] NVARCHAR NOT NULL,
  [address_line_2] NVARCHAR,
  [city_id] INTEGER NOT NULL,
  [postal_code_id] INTEGER NOT NULL,
  [region_id] INTEGER NOT NULL,
  [is_carrier] BIT NOT NULL DEFAULT (0),
  [is_local] BIT NOT NULL DEFAULT (0),
  [is_international] BIT NOT NULL DEFAULT (0)
'''

def createAddressTable(sqlConn):
  addressTable = Table("address", sqlConn)
  addressTable.create(tableFields=tableFields)
  addressTable.commit()

def insertAddressData(sqlConn):
  return