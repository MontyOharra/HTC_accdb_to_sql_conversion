from ...imports import *

addressFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY IDENTITY(1, 1)"),
    Field(fieldName="address_line_1", fieldDetails="NVARCHAR(255) NOT NULL"),
    Field(fieldName="address_line_2", fieldDetails="NVARCHAR(50)"),
    Field(fieldName="city_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="postal_code_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="is_carrier", fieldDetails="BIT NOT NULL DEFAULT (0)"),
    Field(fieldName="is_local", fieldDetails="BIT NOT NULL DEFAULT (0)"),
    Field(fieldName="is_international", fieldDetails="BIT NOT NULL DEFAULT (0)")
]

addressIndexes : List[Index] = [
  Index('ix_city_id', 'city_id', 'nonclustered'),
  Index('ix_postal_code_id', 'postal_code_id', 'nonclustered'),
  Index('ix_street_address', ['address_line_1', 'address_line_2'], 'nonclustered')
]

addressForeignKeys : List[ForeignKey] = [
  ForeignKey('address', 'city_id', 'city', 'id'),
  ForeignKey('address', 'postal_code_id', 'postal_code', 'id')
]

def createAddressTable(conn):
  addressTable = SqlTable('address', conn, addressFields, addressIndexes)
  addressTable.createTable()
  addressTable.addIndexes()
  
  return addressTable
  