from ...imports import *

regionFields: List[Field] = [
    Field('id,' 'INTEGER PRIMARY KEY IDENTITY(1, 1)'),
    Field('region_name', 'NVARCHAR(63) NOT NULL'),
    Field('iso_code', 'NVARCHAR(2) NOT NULL'),
    Field('country_id', 'INTEGER NOT NULL' )
]

regionIndexes: List[Index] = [
    Index('ix_region_name', 'region_name', 'nonclustered', isUnique=True)
]

regionForeignKeys: List[ForeignKey] = [
    ForeignKey('region', 'country_id', 'country')
]

def createregionTable(conn):
    regionTable = SqlTable('region', conn, regionFields, regionIndexes)
    regionTable.createTable()
    regionTable.addIndexes()
    
    return regionTable

def insertRegion(
    conn : Connection,
    countryId: int,
    name : str = None,
    isoCode : str = None,
) :
    if name:
        data = {
            'region_name': name,
            'iso_code': subdivisions_countries.get(name=name)['code'],
            'country_id': countryId
        }
    elif isoCode:
        data = {
            'region_name': subdivisions_countries.get(code=isoCode)['name'],
            'iso_code': isoCode,
            'country_id': countryId
        }
    else:
        data = {
            'region_name': 'Texas',
            'iso_code': 'TX',
            'country_id': 1
        }
        
    conn.sqlInsertRow(
        'region',
        data
    )