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

def insertCountry(
    conn : Connection,
    name : str = None,
    isoCode2 : str = None,
    isoCode3 : str = None
) :
    if name:
        data = {
            'iso_code_2': countries.get(name=name)['alpha_2'],
            'iso_code_3': countries.get(name=name)['alpha_3'],
            'country_name': name
        }
    elif isoCode2:
        data = {
            'iso_code_2': isoCode2,
            'iso_code_3': countries.get(alpha_2=isoCode2)['alpha_3'],
            'country_name': countries.get(alpha_2=isoCode2)['name']
        }
    elif isoCode3:
        data = {
            'iso_code_2': countries.get(alpha_3=isoCode3)['alpha_2'],
            'iso_code_3': isoCode3,
            'country_name': countries.get(alpha_3=isoCode3)['name']
        }
    else:
        data = {
            'iso_code_2': 'US',
            'iso_code_3': 'USA',
            'country_name': 'United States'
        }
        
    conn.sqlInsertRow(
        'country',
        data
    )