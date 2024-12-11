from ...imports import *

from ..sql.address import addAddress
from ..sql.company import addCompany
from ..sql.phone import addPhone
from ..sql.fax import addFax

def convert_HTC000_G010_T010_Company_Info(conn : Connection):
    tableName = 'HTC000_G010_T010 Company Info'
    companyInfo = conn.accessGetTableInfo('htc000', tableName)
    for i, row in enumerate(companyInfo, start=1):
        sys.stdout.write(f"\rConverting [{tableName}] Table: Currently converting row ({i}/{len(companyInfo)})\033[K")
        sys.stdout.flush()
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
            countryDetails={'default': ''}
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
        
    sys.stdout.write(f"\rCompleted [{tableName}] Conversion.\033[K\n")
    sys.stdout.flush()
        