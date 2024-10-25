from ...imports import *

cityFields: List[Field] = [
    Field("id", "INTEGER PRIMARY KEY IDENTITY(1, 1)"),
    Field("city_name", "VARCHAR(63) NOT NULL"),
    Field("lat", "DECIMAL(9, 6) NOT NULL"),
    Field("lng", "DECIMAL(9, 6) NOT NULL"),
    Field("region_id", "INTEGER")
]

cityIndexes : List[Index] = [
  Index('ix_region_id', 'region_id', 'nonclustered')
]

def createCityTable(conn):
  cityTable = SqlTable('city', conn, cityFields, cityIndexes)
  cityTable.createTable()
  cityTable.addIndexes()
  
  return cityTable