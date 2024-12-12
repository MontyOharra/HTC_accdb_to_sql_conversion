from ...imports import *

from ..sql.aci_data import addAciData
from ..sql.city import addCityPostalCode

from ..sql.user import getUserIdFromUsername

def convert_HTC300_G010_T010_DFW_ACI_Data(conn : Connection, row):
        
    cityId, postalCodeId = addCityPostalCode(
        conn,
        cityName=row.CITY_PLACE,
        postalCode=row.ZIP_CODE,
        regionDetails={'isoCode' : row.STATE},
        countryDetails={'countryName' : row.Country}
    )
    
    if not cityId or not postalCodeId:
        return
    
    if row.AREA.strip().upper() == 'HOTSHOT':
        correctArea = '@'
    elif row.AREA.strip() == '':
        correctArea = None
    else:
        correctArea = row.AREA.strip().lower()
    
    addAciData(
        conn,
        aciDataId=row.ID,
        cityId=cityId,
        branchId=row.ACIBrID,
        postalCodeId=postalCodeId,
        airportCode=row.AIRP_CODE,
        carrier=row.CARRIER,
        area=correctArea,
        rateMin=row.RATE_MIN,
        rate100=row.RATE_100,
        rate1000=row.RATE_1000,
        rate2000=row.RATE_2000,
        rate5000=row.RATE_5000,
        dateCreated=row.CreateDate,
        createdBy=getUserIdFromUsername(conn, row.CreatedBy),
        isActive=row.Active
    )