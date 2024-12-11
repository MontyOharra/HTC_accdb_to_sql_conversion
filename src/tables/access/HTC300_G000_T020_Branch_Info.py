from ...imports import *

from ..sql.address import addAddress
from ..sql.phone import addPhone
from ..sql.fax import addFax
from ..sql.branch import addBranch

def convert_HTC300_G000_T020_Branch_Info(conn : Connection):
    tableName = 'HTC300_G000_T020 Branch Info'
    branchInfo = conn.accessGetTableInfo('htc300', tableName)
    for i, row in enumerate(branchInfo, start=1):
        sys.stdout.write(f"\rConverting [{tableName}] Table: Currently converting row ({i}/{len(branchInfo)})\033[K")
        sys.stdout.flush()
        addressId = addAddress(
            conn,
            row.BrAddrLn1,
            row.BrAddrLn2,
            row.BrCity,
            row.BrZip,
            {'isoCode' : row.BrStOrProv},
            {'default' : ''}
        )
        phoneId = addPhone(
            conn,
            '1',
            getPhoneAreaCode(row.BrDispPhone),
            getPhoneNumber(row.BrDispPhone),
            row.BrDispExtension
        )
        faxId = addFax(
            conn,
            '1',
            getPhoneAreaCode(row.BrDispFax),
            getPhoneNumber(row.BrDispFax),
            row.BrDispExtension
        )
        
        addBranch(
            conn,
            branchName=row.BrName,
            companyId=row.BrCoID,
            airportCode=row.BrAirportCode,
            isActive=row.BrActive,
            cartageAgentType=row.BrCartageAgentType,
            fuelServiceCharge=row.BrFSC,
            transferRate=row.BrTrnsfrRate,
            aciLow=row.BrLowACI,
            aciHigh=row.BrHighACI,
            addressId=addressId,
            phoneId=phoneId,
            faxId=faxId,
            email=row.BrDispEmail,
            notes=row.BrNotes,
            internationalAirDimDivisor=row.BrDimFIntlAir,
            domesticAirDimDivisor=row.BrDimFNatlAir,
            truckDimDivisor=row.BrDimfTruck,
        )
    sys.stdout.write(f"\rCompleted [{tableName}] Conversion.\033[K\n")
    sys.stdout.flush()