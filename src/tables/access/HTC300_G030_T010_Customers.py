from ...imports import *

from ..sql.customer import addCustomer
from ..sql.address import addAddress
from ..sql.phone import addPhone
from ..sql.customer_default_assessorial import addCustomerDefaultAssessorial


def convert_HTC300_G030_T010_Customers(conn : Connection, row):  
    cusAddrLine1 = row.Cus_AddrLn1.strip().lower().replace(u'\xa0', u' ')
    cusAddrLine2 = row.Cus_AddrLn2.strip().lower().replace(u'\xa0', u' ')
    cusCity = row.Cus_City.strip().lower().replace(u'\xa0', u' ').replace("'", "''")
    cusZip = row.Cus_Zip.strip().lower().replace(u'\xa0', u' ')
    cusState = row.Cus_State.strip().lower().replace(u'\xa0', u' ')
    if row.Cus_Country == None:
        cusCountry = ''
    else:
        cusCountry = row.Cus_Country.strip().lower().replace(u'\xa0', u' ')
  
    if cusCity == 'mississuaga':    
        addressId = addAddress(
        conn,
        cusAddrLine1,
        cusAddrLine2,
        cusCity,
        cusZip,
        {'isoCode' : 'ON'},
        {'isoCode3' : 'CAN'} 
    )
    else:
      if cusCountry == '':
          if cusState in ['on', 'qc', 'mb']:
            addressId = addAddress(
                conn,
                cusAddrLine1,
                cusAddrLine2,
                cusCity,
                cusZip,
                {'isoCode' : cusState},
                {'isoCode3' : 'CAN'}
            )
          else:
            addressId = addAddress(
                conn,
                cusAddrLine1,
                cusAddrLine2,
                cusCity,
                cusZip,
                regionDetails={'isoCode' : cusState},
                countryDetails={'default' : ''},
            )
      elif cusCountry == 'canada':
        addressId = addAddress(
            conn,
            cusAddrLine1,
            cusAddrLine2,
            cusCity,
            cusZip,
            {'isoCode' : cusState},
            {'isoCode3' : 'CAN'}
        )
      else:
        addressId = addAddress(
            conn,
            cusAddrLine1,
            cusAddrLine2,
            cusCity,
            cusZip,
            regionDetails={'isoCode' : cusState},
            countryDetails={'default' : ''},
        )
    
    phoneId = addPhone(
        conn,
        '1',
        getPhoneAreaCode(row.Cus_Phone),
        getPhoneNumber(row.Cus_Phone),
        row.Cus_Extension
    )
    
    for assessorialId in getAssessorialIds(row.Cus_Assessorials):
        addCustomerDefaultAssessorial(
            conn,
            customerId=row.CustomerID,
            assessorialId=assessorialId
        )
        
    defaultRateId = 1
    
    addCustomer(
        conn,
        customerId=row.CustomerID,
        branchId=row.Cus_BrID,
        customerName=row.Customer,
        addressId=addressId,
        phoneId=phoneId,
        notes=row.Cus_Notes,
        fuelServiceCharge=row.Cus_FSC,
        defaultRateId=defaultRateId,
        isActive=row.Cus_Status,
        isQbInvoiceOmitted=row.Cus_OmitQBInvoice,
        qbCustomerRefId=row.Cus_QBCustomerRefListID,
        qbCustomerRefName=row.Cus_QBCustomerRefFullName,
    )
    