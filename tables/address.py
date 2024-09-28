from typing import Union

from utils.table import Table

tableFields = '''
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

addressTable : Union[Table, None] = None

def createAddressTable(dbConnections):
  global addressTable
  addressTable = Table("address", dbConnections)
  addressTable.createTable(tableFields=tableFields)
  addressTable.commit()

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