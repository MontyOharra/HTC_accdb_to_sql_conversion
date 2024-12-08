from ...imports import *

from ..sql.aci_data import addAciData
from ..sql.city import addCityPostalCode

from ..sql.user import getUserIdFromUsername

def convert_HTC300_G010_T010_DFW_ACI_Data(conn : Connection):
    aci_dataInfo = conn.accessGetTableInfo('htc300', 'HTC300_G010_T010 DFW_ACI_Data')
    for row in aci_dataInfo:
        cityId, postalCodeId = addCityPostalCode(
            conn,
            cityName=row.CITY_PLACE,
            postalCode=row.ZIP_CODE,
            regionDetails={'isoCode' : row.STATE},
            countryDetails={'countryName' : row.Country}
        )
        
        addAciData(
            conn,
            cityId=cityId,
            branchId=row.ACIBrID,
            postalCodeId=postalCodeId,
            airportCode=row.AIRP_CODE,
            carrier=row.CARRIER,
            area=row.AREA,
            rateMin=row.RATE_MIN,
            rate100=row.RATE_100,
            rate1000=row.RATE_1000,
            rate2000=row.RATE_2000,
            rate5000=row.RATE_5000,
            dateCreated=row.CreateDate,
            createdBy=getUserIdFromUsername(conn, row.CreatedBy),
            isActive=row.Active
        )
        
    print('Completed [HTC300_G010_T010 DFW_ACI_Data] Conversion.')