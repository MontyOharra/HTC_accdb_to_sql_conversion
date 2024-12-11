from ...imports import *

from ..sql.aci_data import addAciData
from ..sql.city import addCityPostalCode

from ..sql.user import getUserIdFromUsername

def convert_HTC300_G010_T010_DFW_ACI_Data(conn : Connection):
    tableName = 'HTC300_G010_T010 DFW_ACI_Data'
    aci_dataInfo = conn.accessGetTableInfo('htc300', tableName)
    for i, row in enumerate(aci_dataInfo, start=1):
        sys.stdout.write(f"\rConverting [{tableName}] Table: Currently converting row ({i}/{len(aci_dataInfo)})\033[K")
        sys.stdout.flush()
        
        cityId, postalCodeId = addCityPostalCode(
            conn,
            cityName=row.CITY_PLACE,
            postalCode=row.ZIP_CODE,
            regionDetails={'isoCode' : row.STATE},
            countryDetails={'countryName' : row.Country}
        )
        
        if row.AREA.strip().upper() == 'HOTSHOT':
            correctArea = '@'
        elif row.AREA.strip() == '':
            correctArea = None
        else:
            correctArea = row.AREA.strip().lower()
        
        addAciData(
            conn,
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
        
    sys.stdout.write(f"\rCompleted [{tableName}] Conversion.\033[K\n")
    sys.stdout.flush()