from ...imports import *

from ..sql.address import addAddress
from ..sql.phone import addPhone
from ..sql.fax import addFax
from ..sql.branch import addBranch

def convert_HTC300_G000_T020_Branch_Info(conn : Connection, row):
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
        branchId=row.BrID,
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