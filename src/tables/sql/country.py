from ...imports import *

countryFields: List[Field] = [
    Field('id,' 'INTEGER PRIMARY KEY IDENTITY(1, 1)'),
    Field('country_name', 'NVARCHAR(63) NOT NULL'),
    Field('iso_code_2', 'NVARCHAR(2) NOT NULL'),
    Field('iso_code_3', 'NVARCHAR(2) NOT NULL' )
]

countryIndexes: List[Index] = [
    Index('ix_country_name', 'country_name', 'nonclustered', isUnique=True)
]

def createCountryTable(conn):
    countryTable = SqlTable('country', conn, countryFields, countryIndexes)
    countryTable.createTable()
    countryTable.addIndexes()
    
    return countryTable