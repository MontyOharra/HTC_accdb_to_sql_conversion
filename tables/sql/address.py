from ...classes.Connection import Connection
from ...classes.sqlTable import SqlTable

from ...types.Field import Field
from ...types.ForeignKey import ForeignKey
from ...types.Index import Index

from typing import List

addressFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY IDENTITY(1, 1)"),
    Field(fieldName="address_line_1", fieldDetails="NVARCHAR(255) NOT NULL"),
    Field(fieldName="address_line_2", fieldDetails="NVARCHAR(50)"),
    Field(fieldName="city_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="postal_code_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="region_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="is_carrier", fieldDetails="BIT NOT NULL DEFAULT (0)"),
    Field(fieldName="is_local", fieldDetails="BIT NOT NULL DEFAULT (0)"),
    Field(fieldName="is_international", fieldDetails="BIT NOT NULL DEFAULT (0)")
]

addressIndexes = {
  'ix_city': {
    'tableName': 'address',
    'indexType': 'nonclustered',
    'indexField': 'city_id'
  }
}

def createAddressTable(conn):
  return SqlTable('address', conn, addressFields, addressIndexes)