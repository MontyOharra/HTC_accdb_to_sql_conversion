from ...imports import *

from ..sql.city import addCityPostalCode
from ..sql.region import addRegion
from ..sql.country import addCountry

def convert_HTC010_G000_T000_US_Zip_Codes(conn : Connection):
    tableName = 'HTC010_G000_T000 US Zip Codes'
    zipCodeInfo = conn.accessGetTableInfo('htc010', tableName)
    for i, row in enumerate(zipCodeInfo, start=1):
        sys.stdout.write(f"\rConverting [{tableName}] Table: Currently converting row ({i}/{len(zipCodeInfo)})\033[K")
        sys.stdout.flush()
        if row.ZipCodeType == 'MILITARY':
            continue
        if row.State in [
            'AB', 'BC', 'MB', 'NB', 'NL',
            'NT', 'NS', 'NU', 'ON', 'PE',
            'QC', 'SK', 'YT'
        ]:
          addCityPostalCode(
              conn,
              cityName=row.City,
              postalCode=row.Zipcode,
              regionDetails={'isoCode' : row.State},
              countryDetails={'countryName' : 'Canada'}
          )
        else:
          addCityPostalCode(
              conn,
              cityName=row.City,
              postalCode=row.Zipcode,
              regionDetails={'isoCode' : row.State},
              countryDetails={'default' : ''}
          )
    sys.stdout.write(f"\rCompleted [{tableName}] Conversion.\033[K\n")
    sys.stdout.flush()