from ...imports import *

from isocodes import subdivisions_countries

from .country import addCountry

def regionGet(**kwargs: str):
    try:
        key: str = next(iter(kwargs))
        return [
            element
            for element in subdivisions_countries.data
            if key in element and kwargs[key].lower() == element[key].lower()
        ]
    except IndexError:
        return {}
    
regionFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="country_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="iso_code", fieldDetails="NVARCHAR(6) NOT NULL"),
    Field(fieldName="region_name", fieldDetails="NVARCHAR(63) NOT NULL"),
]

regionIndexes: List[Index] = [
]

regionForeignKeys: List[ForeignKey] = [
    ForeignKey('region', 'country_id', 'country', 'id'),
]

def createRegionTable(conn):
    regionTable = SqlTable('region', conn, regionFields, regionIndexes, regionForeignKeys)
    regionTable.createTable()
    regionTable.addIndexes()

    return regionTable


def addRegion(
    conn : Connection,
    regionDetails : Dict[str, str],
    countryDetails : Dict[str, str]
) -> int : 
    if not regionDetails or not countryDetails:
        return 0
    
    countryId = addCountry(conn, countryDetails=countryDetails)
    countryIsoCode = conn.sqlGetInfo('country', 'iso_code_2', f"[id] = '{countryId}'")[0].iso_code_2
    
    if 'regionName' in regionDetails:
        regionName = regionDetails['regionName'].lower()
        regionRow = conn.sqlGetInfo('region', 'id', f"[region_name] = '{regionName}' AND [country_id] = {countryId}")
        if regionRow:
            return regionRow[0].id
        
        for region in regionGet(name=regionName):
            if region['code'][0:1].lower() == countryIsoCode:
                correctRegion = region
                break
        data = {
            'region_name' : regionName,
            'iso_code' : correctRegion[3:].lower(),
            'country_id' : countryId
        } 
    elif 'isoCode' in regionDetails:
        isoCode = regionDetails['isoCode'].lower()
        regionRow = conn.sqlGetInfo('region', 'id', f"[iso_code] = '{isoCode}' AND [country_id] = '{countryId}'")
        if regionRow:
            return regionRow[0].id
        data = {
            'region_name': regionGet(code=f'{countryIsoCode}-{isoCode}'.upper())[0]['name'].lower(),
            'iso_code' : isoCode,
            'country_id' : countryId
        }
        
    conn.sqlInsertRow('region', data)    
    conn.commit()
    
    return conn.sqlGetLastIdCreated('region')