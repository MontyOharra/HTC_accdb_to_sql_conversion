from ...imports import *

from .country import addCountry
from .region import addRegion
from .city import addCityPostalCode

addressFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="address_line_1", fieldDetails="NVARCHAR(127) NOT NULL"),
    Field(fieldName="address_line_2", fieldDetails="NVARCHAR(63)"),
    Field(fieldName="city_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="postal_code_id", fieldDetails="INTEGER NOT NULL"),
]

addressIndexes: List[Index] = [
]

addressForeignKeys: List[ForeignKey] = [
    ForeignKey('address', 'city_id', 'city', 'id'),
    ForeignKey('address', 'postal_code_id', 'postal_code', 'id'),
]

def createAddressTable(conn):
    addressTable = SqlTable('address', conn, addressFields, addressIndexes, addressForeignKeys)
    addressTable.createTable()
    addressTable.addIndexes()

    return addressTable


def addAddress(
    conn : Connection,
    addressLine1 : str,
    addressLine2 : str,
    cityName : str,
    postalCode : str,
    regionDetails : Dict[str, any],
    countryDetails : Dict[str, any]
):

    if not addressLine1 or not cityName or not postalCode or not regionDetails or not countryDetails:
        return None
    
    addressLine1 = addressLine1.lower()
    if type(addressLine2) == str:
        addressLine2 = addressLine2.lower()
        if addressLine2.strip() == '':
            addressLine2 = None
        
    cityId, postalCodeId = addCityPostalCode(conn, cityName, postalCode, regionDetails=regionDetails, countryDetails=countryDetails)
    
    addressRow = conn.sqlGetInfo(
        'address',
        'id',
        whereDetails={
            'address_line_1': addressLine1,
            'address_line_2': addressLine2,
            'city_id': cityId,
            'postal_code_id': postalCodeId
        }
    )
    if addressRow:
        return addressRow[0].id
    
    addressData = {
        'address_line_1' : addressLine1,
        'address_line_2' : addressLine2,
        'city_id' : cityId,
        'postal_code_id' : postalCodeId
    }
    
    conn.sqlInsertRow('address', addressData)
    conn.commit()
    
    return conn.sqlGetLastIdCreated('address')