from ...imports import *

from isocodes import countries

def countryGet(**kwargs: str):
    try:
        key: str = next(iter(kwargs))
        res = [
            element
            for element in countries.data
            if key in element and kwargs[key].lower() == element[key].lower()
        ]
        return res
        
    except IndexError:
        return {}
    
countryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="country_name", fieldDetails="NVARCHAR(63) UNIQUE NOT NULL"),
    Field(fieldName="iso_code_2", fieldDetails="NVARCHAR(2) UNIQUE NOT NULL"),
    Field(fieldName="iso_code_3", fieldDetails="NVARCHAR(3) UNIQUE NOT NULL"),
]

countryIndexes: List[Index] = [
]

countryForeignKeys: List[ForeignKey] = [
]

def createCountryTable(conn):
    countryTable = SqlTable('country', conn, countryFields, countryIndexes, countryForeignKeys)
    countryTable.createTable()
    countryTable.addIndexes()

    return countryTable

def addCountry(
    conn : Connection,
    countryDetails : Dict[str, str]
) -> int:    
    if not countryDetails:
        return 0
    if 'countryName' in countryDetails:
        countryName = countryDetails['countryName'].lower()
        countryRow = conn.sqlGetInfo('country', 'id', f"[country_name] = '{countryName}'")
        if countryRow:
            return countryRow[0].id
        data = {
            'iso_code_2': countryGet(name=countryName)[0]['alpha_2'].lower(),
            'iso_code_3': countryGet(name=countryName)[0]['alpha_3'].lower(),
            'country_name': countryName
        }
    elif 'isoCode2' in countryDetails:
        isoCode2 = countryDetails['isoCode2'].lower()
        countryRow = conn.sqlGetInfo('country', 'id', f"[iso_code_2] = '{isoCode2}'")
        if countryRow:
            return countryRow[0].id
        data = {
            'iso_code_2': isoCode2,
            'iso_code_3': countryGet(alpha_2=isoCode2)[0]['alpha_3'].lower(),
            'country_name': countryGet(alpha_2=isoCode2)[0]['name'].lower()
        }
    elif 'isoCode3' in countryDetails:
        isoCode3 = countryDetails['isoCode3'].lower()
        countryRow = conn.sqlGetInfo('country', 'id', f"[iso_code_3] = '{isoCode3}'")
        if countryRow:
            return countryRow[0].id
        data = {
            'iso_code_2': countryGet(alpha_3=isoCode3)[0]['alpha_2'].lower(),
            'iso_code_3': isoCode3,
            'country_name': countryGet(alpha_3=isoCode3)[0]['name'].lower()
        }
    elif 'default' in countryDetails:
        countryRow = conn.sqlGetInfo('country', 'id', f"[iso_code_2] = 'us'")
        if countryRow:
            return countryRow[0].id
        data = {
            'iso_code_2': 'us',
            'iso_code_3': 'usa',
            'country_name': 'united states'
        }
        
    conn.sqlInsertRow('country', data)
    conn.commit()
    
    return conn.sqlGetLastIdCreated('country')