from ...imports import *

from ..sql.region import addRegion

cityFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="city_name", fieldDetails="NVARCHAR(63) NOT NULL"),
]

cityIndexes: List[Index] = [
]

cityForeignKeys: List[ForeignKey] = [
]

def createCityTable(conn):
    cityTable = SqlTable('city', conn, cityFields, cityIndexes, cityForeignKeys)
    cityTable.createTable()
    cityTable.addIndexes()

    return cityTable

def addCityPostalCode(
    conn : Connection,
    cityName : str,
    postalCode : str,
    regionDetails : Dict[str, str],
    countryDetails : Dict[str, str]
) -> Tuple[int] :
    
    if not cityName or not postalCode or not regionDetails or not countryDetails:
        return (0, 0)
    
    cityName = cityName.lower()
    postalCode = postalCode.lower()
    
    regionId = addRegion(conn, regionDetails, countryDetails)
    
    cityRow = conn.sqlGetInfo('city INNER JOIN city_region ON [city].[id] = [city_region].[city_id]', '[city].[id] AS selected_city_id', f"[city].[city_name] = '{cityName}' AND [city_region].[region_id] = '{regionId}'")
    postalCodeRow = conn.sqlGetInfo('postal_code INNER JOIN postal_code_region ON [postal_code].id = [postal_code_region].[postal_code_id]', '[postal_code].[id] AS selected_postal_code_id', f"[postal_code].[postal_code] = '{postalCode}' AND [postal_code_region].[region_id] = '{regionId}'")
    if cityRow:
        cityId = cityRow[0].selected_city_id
    else:
        cityData = {
            'city_name' : cityName
        }
        conn.sqlInsertRow('city', cityData)
        conn.commit()
        
        cityId = conn.sqlGetLastIdCreated('city')
    if postalCodeRow:
        postalCodeId = postalCodeRow[0].selected_postal_code_id
    else:
        postalCodeData = {
            'postal_code' : postalCode
        }
        conn.sqlInsertRow('postal_code', postalCodeData)
        conn.commit()
        
        postalCodeId = conn.sqlGetLastIdCreated('postal_code')
        
    if cityRow and postalCodeRow:
        return (cityId, postalCodeId)
    
    cityRegionData = {
        'city_id' : cityId,
        'region_id' : regionId
    }
    conn.sqlInsertRow('city_region', cityRegionData)
    conn.commit()
        
    postalCodeRegionData = {
        'postal_code_id' : postalCodeId,
        'region_id' : regionId
    }
    conn.sqlInsertRow('postal_code_region', postalCodeRegionData)
    conn.commit()
    
    cityPostalCodeData = {
        'city_id' : cityId,
        'postal_code_id' : postalCodeId,
        'lat' : getCityLat(cityName=cityName, postalCode=postalCode),
        'lng' : getCityLat(cityName=cityName, postalCode=postalCode)
    }
    conn.sqlInsertRow('city_postal_code', cityPostalCodeData)
    conn.commit()
    
    return (cityId, postalCodeId)