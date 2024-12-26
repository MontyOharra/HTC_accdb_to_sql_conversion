from ...imports import *

from ..sql.city import addCityPostalCode
from ..sql.region import addRegion
from ..sql.country import addCountry

def convert_HTC010_G000_T000_US_Zip_Codes(conn : Connection, row):
    if row.ZipCodeType == 'MILITARY':
        return
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