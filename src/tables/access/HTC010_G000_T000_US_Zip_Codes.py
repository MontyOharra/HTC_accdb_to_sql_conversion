from ...imports import *

from ..sql.city import addCityPostalCode
from ..sql.region import addRegion
from ..sql.country import addCountry

def convert_HTC010_G000_T000_US_Zip_Codes(conn : Connection):
    zipCodeInfo = conn.accessGetTableInfo('htc010', 'HTC010_G000_T000 US Zip Codes')
    for row in zipCodeInfo:
        if row.ZipCodeType == 'MILITARY':
            continue
        if row.State in [
            'AB', 'BC', 'MB', 'NB', 'NL',
            'NT', 'NS', 'NU', 'ON', 'PE',
            'QC', 'SK', 'YT'
        ]:
            countryId = addCountry(
                conn,
                countryName='Canada'
            )
        else:
            countryId = 1
        regionId = addRegion(
            conn,
            countryId=countryId,
            isoCode=row.State
        )
        addCityPostalCode(
            conn,
            cityName=row.City,
            postalCode=row.Zipcode,
            regionId=regionId
        )
    print('Completed [HTC010_G000_T000 US Zip Codes] Conversion.')