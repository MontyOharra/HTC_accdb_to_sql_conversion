from ...imports import *

from ..sql.customer import addCustomer
from ..sql.address import addAddress
from ..sql.phone import addPhone

def convert_HTC300_G030_T010_Customers(conn : Connection, row):
    addressId = addAddress(
        conn,
        row.Cus_AddrLn1,
        row.Cus_AddrLn2,
        row.Cus_City,
        row.Cus_Zip,
        {'isoCode' : row.Cus_State},
        {'isoCode3' : row.Cus_Country} 
    )
    
    phoneId = addPhone(
        conn,
        '1',
        getPhoneAreaCode(row.Cus_Phone),
        getPhoneNumber(row.Cus_Phone),
        row.Cus_Extension
    )
    
    addCustomer(
        conn,
        customerId=row.CustomerId,
        branchId=row.Cus_BrId,
        customerName=row.Customer,
        addressId=addressId,
        phoneId=phoneId,
        notes=row.Cus_Notes,
        fuelServiceCharge=row.Cus_FSC,
        defaultRateId=1, # FIXXXXXX!!!!
        isActive=row.Cus_Status,
        isQbInvoiceOmitted=row.Cus_OmitQBInvoice,
        qbCustomerRefId=row.Cus_QBCustomerRefListID,
        qbCustomerRefName=row.Cus_QBCustomerRefFullName
    )