from typing import Dict, List
from classes.Connection import Connection

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

    conn.sqlCreateTable(tableName, fields)
    conn.commit()

  def addIndexes(self):
    for index in self.indexes:
      self.conn.sqlAddIndex(self.tableName, index.indexType, index.indexField, index.indexName, index.isUnique)

  def addForeignKeys(self):
    for key in self.foreignKeys:
      self.conn.sqlAddForeignKey(self.tableName, key.fromTableField, key.toTableName, key.toTableField)


