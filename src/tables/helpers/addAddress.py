from imports import Connection, Dict
from geocoding import getLat, getLng

from isocodes import countries, subdivisions_countries


def addAddress(
    conn : Connection,
    addressLine1 : str, 
    addressLine2 : str,
    city : str,
    postalCode : str,
    regionDetails : Dict[str],
    countryDetails : Dict[str],
    isCarrier : bool = False,
    isLocal : bool = False,
    isInternational : bool = False
):
    
    if len(list(countryDetails.keys())) > 1 or len(list(regionDetails.keys())) > 1:
        print('Please only include one value for each detail field.')
        return None
    
    # Populate country table
    if countryDetails['iso2']:
        countryDetail = countryDetails['iso2']
        conn.sqlInsertRow(
            'country',
            {
                'iso_code_2' : countryDetail,
                'iso_code_3' : countries.get(alpha_2=countryDetail)['alpha_3'],
                'country_name' : countries.get(alpha_2=countryDetail)['name']
            }   
        )
        countryId = conn.getIdFromFieldValue('country', 'iso_code_2', countryDetail)
    elif countryDetails['iso3']:
        countryDetail = countryDetails['iso3']
        conn.sqlInsertRow(
            'country',
            {
                'iso_code_2' : countries.get(alpha_3=countryDetail)['alpha_2'],
                'iso_code_3' : countryDetail,
                'country_name' : countries.get(alpha_3=countryDetail)['name']
            }   
        )
        countryId = conn.getIdFromFieldValue('country', 'iso_code_3', countryDetail)
    elif countryDetails['name']:
        countryDetail = countryDetails['name']
        conn.sqlInsertRow(
            'country',
            {
                'iso_code_2' : countries.get(name=countryDetail)['alpha_2'],
                'iso_code_3' : countries.get(name=countryDetail)['alpha_3'],
                'country_name' : countryDetail
            }
        )
        countryId = conn.getIdFromFieldValue('country', 'name', countryDetail)
     
    # Populate region table   
    if regionDetails['name']:
        regionDetail = regionDetails['name']
        conn.sqlInsertRow(
            'region',
            {
                'iso_code': subdivisions_countries.get(name=regionDetail)['code'],
                'region_name': regionDetail,
                'country_id': countryId
            }
        )
        regionId = conn.getIdFromFieldValue('region', 'name', regionDetail)
    elif regionDetails['iso_code']:
        regionDetail = regionDetails['iso_code']
        conn.sqlInsertRow(
            'region',
            {
                'iso_code': regionDetail,
                'region_name': subdivisions_countries.get(name=regionDetail)['name'],
                'country_id': countryId
            }
        )
        regionId = conn.getIdFromFieldValue('region', 'iso_code', regionDetail)
        
    # Populate postal_code table
    conn.sqlInsertRow(
        'postal_code',
        {
            'postal_code': postalCode,
            'region_id': regionId
        }
    )
    postalCodeId = conn.getIdFromFieldValue('postal_code', 'postal_code', postalCode)
    
    conn.sqlInsertRow(
        'city',
        {
            'city_name': city,
            'lat': getLat('city', city),
            'lng': getLng('city', city),
            'region_id': regionId
        }
    )
    cityId = conn.getIdFromFieldValue('city', 'city_name', city)
    
    conn.sqlInsertRow(
        'city_postal_code',
        {
            'city_id': cityId,
            'postal_code_id': postalCodeId
        }
    )
    
    conn.sqlInsertRow(
        'address',
        {
            'address_line_1': addressLine1,
            'address_line_2': addressLine2,
            'city_id': cityId,
            'postal_code_id': postalCodeId,
            'is_carrier': isCarrier,
            'is_local': isLocal,
            'is_international': isInternational
        }
    )