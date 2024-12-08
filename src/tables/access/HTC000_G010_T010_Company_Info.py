from ...imports import *

from ..sql.address import addAddress
from ..sql.company import addCompany
from ..sql.phone import addPhone
from ..sql.fax import addFax

def convert_HTC000_G010_T010_Company_Info(conn : Connection):
    companyInfo = conn.accessGetTableInfo('htc000', 'HTC000_G010_T010 Company Info')
    for row in companyInfo:
        phoneId = addPhone(
            conn,
            countryCode='1',
            areaCode=getPhoneAreaCode(row.CoOfcrPhone),
            phoneNumber=getPhoneNumber(row.CoOfcrPhone),
            phoneExtension=row.CoOfcrExtension
        )
        faxId = addFax(
            conn,
            countryCode='1',
            areaCode=getPhoneAreaCode(row.CoFax),
            faxNumber=getPhoneNumber(row.CoFax),
            faxExtension=''
        )
        
        addressId = addAddress(
            conn,
            addressLine1=row.CoMailAddrLn1,
            addressLine2=row.CoMailAddrLn2,
            cityName=row.CoMailCity,
            postalCode=correctPostalCode(row.CoMailZip),
            regionDetails={'isoCode' : row.CoMailState},
            countryDetails={}
        )
        
        addCompany(
            conn,
            companyName=row.CoName,
            isActive=row.CoActive,
            scac=row.CoSCAC,
            employerIdentificationNo=row.CoTaxID,
            website=row.CoWebPage,
            isTsaCompliant=row.CoTSACompliant,
            airportCode=row.CoAirportCode,
            cartageAgentType=row.CoCartageAgentType,
            logoPath=row.CoLogo,
            addressId=addressId,
            phoneId=phoneId,
            faxId=faxId,
            email=row.CoOfcrEmail,
            notes=row.CoNotes
        )
        
    print('Completed HTC000_G010_T010 Company Info Conversion.')
        