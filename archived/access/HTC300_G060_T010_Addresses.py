from ...imports import *

from ..sql.location import addLocation
from ..sql.address import addAddress
from ..sql.phone import addPhone
from ..sql.location_default_assessorial import addLocationDefaultAssessorial
def convert_HTC300_G060_T010_Addresses(conn : Connection, row):
    addressId = addAddress(
        conn,
        addressLine1=row.FavAddrLn1,
        addressLine2=row.FavAddrLn2,
        cityName=row.FavCity,
        postalCode=row.FavZip,
        regionDetails={'isoCode', row.FavState},
        countryDetails={'isoCode3', row.FavCountry}
    )
    
    phoneId = addPhone(
        conn,
        countryCode='1',
        areaCode=getPhoneAreaCode(row.FavPhone),
        phoneNumber=getPhoneNumber(row.FavPhone),
        phoneExtension=row.FavExt
    )
    
    for assessorialId in getAssessorialIds(row.FavAssessorials):
        addLocationDefaultAssessorial(
            conn,
            locationId=row.FavID,
            assessorialId=assessorialId
        )
    
    addLocation(
        conn,
        locationId=row.FavID,
        branchId=row.FavBRID,
        companyName=row.FavCompany,
        locationName=row.FavLocnName,
        addressId=addressId,
        aciId=row.FavACIID if row.FavACIID != 0 else None,
        contactFirstName=row.FavFirstName,
        contactLastName=row.FavLastName,
        contactEmail=row.FavEMail,
        phoneId=phoneId,
        isCarrier=row.FavCarrierYN,
        isInternational=row.FavInternational,
        defaultWaitTime=row.FavWaitTimeDefault,
        isActive=row.FavActive,
        
    )