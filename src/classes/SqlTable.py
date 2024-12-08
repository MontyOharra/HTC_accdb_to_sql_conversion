from typing import Dict, List
from .Connection import Connection

from ..types.Index import Index
from ..types.ForeignKey import ForeignKey
from ..types.Field import Field

class SqlTable:
  def __init__(self, 
    tableName : str,
    conn : Connection,
    fields : List[Field],
    indexes: List[Index] = [],
    foreignKeys : List[ForeignKey] = []
  ):
    
    self.tableName = tableName
    self.conn = conn
    self.fields = fields
    self.indexes = indexes
    self.foreignKeys = foreignKeys

  def createTable(self):
    self.conn.sqlCreateTable(self.tableName, self.fields)
    self.conn.commit()
    
    print(f'Successfully created [{self.tableName}] table.')

  def addIndexes(self):
    for index in self.indexes:
      self.conn.sqlAddIndex(self.tableName, index.indexType, index.indexFields, index.indexName, index.isUnique)

  def addForeignKeys(self):
    for key in self.foreignKeys:
      self.conn.sqlAddForeignKey(self.tableName, key.fromTableField, key.toTableName, key.toTableField)


