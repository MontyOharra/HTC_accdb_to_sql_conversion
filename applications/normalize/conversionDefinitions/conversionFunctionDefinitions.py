from .addDataFunctionDefinitions import *

def convert_HTC000_G010_T010_Company_Info(conn : Connection, row):
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
        companyId=row.CoID,
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

def convert_HTC000_G025_T010_Positions(conn : Connection, row):
    addPosition(
        conn,
        positionId=row.Posn_ID,
        positionName=row.Posn_Title,
        securityLevel=row.Posn_SecurityLevel,
        isActive=row.Posn_Status,
        branchId=row.Posn_BrID
    )
    
def convert_HTC000_G090_T010_Staff(conn : Connection, row):
    phoneMainId = addPhone(
        conn,
        '1',
        getPhoneAreaCode(row.Staff_Phone),
        getPhoneNumber(row.Staff_Phone),
        ''
    )
    phoneMobileId = addPhone(
        conn,
        '1',
        getPhoneAreaCode(row.Staff_Mobile),
        getPhoneNumber(row.Staff_Mobile),
        ''
    )
    phoneHomeId = addPhone(
        conn,
        '1',
        getPhoneAreaCode(row.Staff_Home_Phone),
        getPhoneNumber(row.Staff_Home_Phone),
        ''
    )
    addressId = addAddress(
        conn,
        row.Staff_Home_Street1,
        row.Staff_Home_Street2,
        row.Staff_Home_City,
        correctPostalCode(row.Staff_Home_Zip),
        {'isoCode' : row.Staff_Home_StAbbr},
        {'isoCode3' : row.Staff_Home_Country}
    )
    
    if row.Staff_Password.strip() == '':
        passwordHash = ""
        passwordSalt = ""
    else:
        passwordSalt = generatePasswordSalt()
        passwordHash = generatePasswordHash(row.Staff_Password.strip(), passwordSalt)
    
    addUser(
        conn,
        userId=row.Staff_EmpID,
        branchId=row.Staff_BrID,
        username=row.Staff_Login,
        namePrefix=row.Staff_NamePrefix if row.Staff_NamePrefix else None,
        firstName=row.Staff_FirstName,
        lastName=row.Staff_LastName,
        nameSuffix=row.Staff_NameSuffix if row.Staff_NamePrefix else None,
        email=row.Staff_Email,
        phoneMainId=phoneMainId,
        phoneMobileId=phoneMobileId,
        tsaType=row.Staff_TSA_Type if row.Staff_NamePrefix else None,
        tsaNumber=row.Staff_TSA_Number if row.Staff_NamePrefix else None,
        tsaTaken=row.Staff_TSA_Taken,
        positionId=row.Staff_RoleID,
        commissionRate=row.Staff_CommRate,
        addressId=addressId,
        phoneHomeId=phoneHomeId,
        dateHired=row.Staff_DateOfHire,
        dateTerminated=row.Staff_DateOfTermination,
        passwordHash=passwordHash,
        passwordSalt=passwordSalt,
        isSecurityCoordinator=row.Staff_SecCoord,
        isTsaTrainer=row.Staff_TSATrainer,
        isDefaultDocOwner=row.Staff_DefaultDocOwner,
        isActive=row.Staff_Active
    )
    
def convert_HTC010_G000_T000_OrderType_Values(conn : Connection, row):
    addOrderType(
        conn,
        orderTypeId=row.OrdType_ID,
        orderTypeName=row.OrdType_Title
    )
    
def convert_HTC010_G000_T000_US_Zip_Codes(conn : Connection, row):
    if row.ZipCodeType == 'MILITARY':
        return
    if row.State in [
        'AB', 'BC', 'MB', 'NB', 'NL',
        'NT', 'NS', 'NU', 'ON', 'PE',
        'QC', 'SK', 'YT'
    ]:
      addCityPostalCode(
          conn,
          cityName=row.City,
          postalCode=row.Zipcode,
          regionDetails={'isoCode' : row.State},
          countryDetails={'countryName' : 'Canada'}
      )
    else:
      addCityPostalCode(
          conn,
          cityName=row.City,
          postalCode=row.Zipcode,
          regionDetails={'isoCode' : row.State},
          countryDetails={'default' : ''}
      )
      
def convert_HTC010_G100_T010_Certification_Test_Catalog(conn : Connection, row):
    addCertificationTest(
      conn,
      certificationTestId=row.TestID,
      certificationName=row.TestTitle,
      certificationTestTrainerId=row.TestTrainerID,
      isActive=row.TestStatus
    )
      
def convert_HTC300_G000_T000_Archive_Update_History(conn : Connection, row):
    addArchiveHistory(
        conn,
        dateArchived=row.ArcCnt_Date,
        openOrders=int(row.ArcCnt_OpnOrd) if row.ArcCnt_OpnOrd != None else 0,
        openOrderAssessorials=int(row.ArcCnt_OpnAss) if row.ArcCnt_OpnAss != None else 0 ,
        openOrderDimensions=int(row.ArcCnt_OpnDim) if row.ArcCnt_OpnDim != None else 0 ,
        openOrderDrivers=int(row.ArcCnt_OpnDvr) if row.ArcCnt_OpnDvr != None else 0 ,
        openOrderAttachments=int(row.ArcCnt_OpnAtt) if row.ArcCnt_OpnAtt != None else 0 ,
        invoicedOrders=int(row.ArcCnt_InvOrd) if row.ArcCnt_InvOrd != None else 0 ,
        invoicedOrderAssessorials=int(row.ArcCnt_InvAss) if row.ArcCnt_InvAss != None else 0 ,
        invoicedOrderDimensions=int(row.ArcCnt_InvDim) if row.ArcCnt_InvDim != None else 0 ,
        invoicedOrderDrivers=int(row.ArcCnt_InvDvr) if row.ArcCnt_InvDvr != None else 0 ,
        invoicedOrderAttachments=int(row.ArcCnt_InvATT) if row.ArcCnt_InvATT != None else 0 ,
        remainingOrders=int(row.ArcCnt_RemOrd) if row.ArcCnt_RemOrd != None else 0 ,
        remainingOrderAssessorials=int(row.ArcCnt_RemAss) if row.ArcCnt_RemAss != None else 0 ,
        remainingOrderDimensions=int(row.ArcCnt_RemDim) if row.ArcCnt_RemDim != None else 0 ,
        remainingOrderDrivers=int(row.ArcCnt_RemDvr) if row.ArcCnt_RemDvr != None else 0 ,
        remainingOrderAttachments=int(row.ArcCnt_RemATT) if row.ArcCnt_RemATT != None else 0 ,
        dockOrders=int(row.ArcCnt_DckOrd) if row.ArcCnt_DckOrd != None else 0 ,
        dockOrderAssessorials=int(row.ArcCnt_DckAss) if row.ArcCnt_DckAss != None else 0 ,
        dockOrderDimensions=int(row.ArcCnt_DckDim) if row.ArcCnt_DckDim != None else 0 ,
        dockOrderDrivers=int(row.ArcCnt_DckDvr) if row.ArcCnt_DckDvr != None else 0 ,
        dockOrderAttachments=int(row.ArcCnt_DckATT) if row.ArcCnt_DckATT != None else 0 ,
        serviceOrders=int(row.ArcCnt_SvcOrd) if row.ArcCnt_SvcOrd != None else 0 ,
        serviceOrderAssessorials=int(row.ArcCnt_SvcAss) if row.ArcCnt_SvcAss != None else 0 ,
        serviceOrderDimensions=int(row.ArcCnt_SvcDim) if row.ArcCnt_SvcDim != None else 0 ,
        serviceOrderDrivers=int(row.ArcCnt_SvcDvr) if row.ArcCnt_SvcDvr != None else 0 ,
        serviceOrderAttachments=int(row.ArcCnt_SvcATT) if row.ArcCnt_SvcATT != None else 0 ,
        activeOrderHistory=int(row.ArcCnt_ActiveHist) if row.ArcCnt_ActiveHist != None else 0 ,
        activeOrderHawbs=int(row.ArcCnt_ActiveHAWB) if row.ArcCnt_ActiveHAWB != None else 0 ,
        archivedOrders=int(row.ArcCnt_ArcOrd) if row.ArcCnt_ArcOrd != None else 0 ,
        archivedOrderAssessorials=int(row.ArcCnt_ArcAss) if row.ArcCnt_ArcAss != None else 0 ,
        archivedOrderDimensions=int(row.ArcCnt_ArcDim) if row.ArcCnt_ArcDim != None else 0 ,
        archivedOrderDrivers=int(row.ArcCnt_ArcDvr) if row.ArcCnt_ArcDvr != None else 0 ,
        archivedOrderAttachments=int(row.ArcCnt_ArcATT) if row.ArcCnt_ArcATT != None else 0 ,
        archivedOrderHistory=int(row.ArcCnt_AchiveHist) if row.ArcCnt_AchiveHist != None else 0 ,
        archivedOrderHawbs=int(row.ArcCnt_ArchiveHAWB) if row.ArcCnt_ArchiveHAWB != None else 0 ,
        removedOrders=int(row.ArcCnt_RmvdOrders) if row.ArcCnt_RmvdOrders != None else 0 ,
        removedOrderAssessorials=int(row.ArcCnt_RmvdAss) if row.ArcCnt_RmvdAss != None else 0 ,
        removedOrderDimensions=int(row.ArcCnt_RmvdDims) if row.ArcCnt_RmvdDims != None else 0 ,
        removedOrderDrivers=int(row.ArcCnt_RmvdDvrs) if row.ArcCnt_RmvdDvrs != None else 0 ,
        removedOrderAttachments=int(row.ArcCnt_RmvdAtts) if row.ArcCnt_RmvdAtts != None else 0 ,
        removedOrderHistory=int(row.ArcCnt_RmvdHist) if row.ArcCnt_RmvdHist != None else 0 ,
        removedOrderHawbs=int(row.ArcCnt_RmvdHAWB) if row.ArcCnt_RmvdHAWB != None else 0 ,
    )

def convert_HTC300_G000_T000_Holidays(conn : Connection, row):
    addHoliday(
        conn,
        holidayName=row.HolidayName,
        holidayDate=row.HolidayDate
    )
    
def convert_HTC300_G000_T000_Over_Night_Update_History(conn : Connection, row):
    userId = getUserIdFromUsername(conn, row.ONUser)
    
    addOvernightMaintenanceHistory(
        conn,
        dateOvernightMaintenance=row.ONDate,
        userId=userId,
        openOrdersIn=int(row.ONOpenOIn),
        openOrderAssessorialsIn=int(row.ONOpenAIn),
        openOrderDimensionsIn=int(row.ONOpenDIn),
        openOrderDriversIn=int(row.ONOpenDvIn),
        openOrderAttachmentsIn=int(row.ONOpenAtIn),
        invoicedOrdersIn=int(row.ONInvOIn),
        invoicedOrderAssessorialsIn=int(row.ONInvAIn),
        invoicedOrderDimensionsIn=int(row.ONInvDIn),
        invoicedOrderDriversIn=int(row.ONInvDvIn),
        invoicedOrderAttachmentsIn=int(row.ONInvAtIn),
        remainingOrdersIn=int(row.ONRemOIn),
        remainingOrderAssessorialsIn=int(row.ONRemAIn),
        remainingOrderDimensionsIn=int(row.ONRemDIn),
        remainingOrderDriversIn=int(row.ONRemDvIn),
        remainingOrderAttachmentsIn=int(row.ONRemAtIn),
        openOrdersOut=int(row.ONOpenOOut),
        openOrderAssessorialsOut=int(row.ONOpenAOut),
        openOrderDimensionsOut=int(row.ONOpenDOut),
        openOrderDriversOut=int(row.ONOpenDVOut),
        openOrderAttachmentsOut=int(row.ONOpenAtOut),
        invoicedOrdersOut=int(row.ONInvOOut),
        invoicedOrderAssessorialsOut=int(row.ONInvAOut),
        invoicedOrderDimensionsOut=int(row.ONInvDOut),
        invoicedOrderDriversOut=int(row.ONInvDVOut),
        invoicedOrderAttachmentsOut=int(row.ONInvAtOut),
        remainingOrdersOut=int(row.ONRemOOut),
        remainingOrderAssessorialsOut=int(row.ONRemAOut),
        remainingOrderDimensionsOut=int(row.ONRemDOut),
        remainingOrderDriversOut=int(row.ONRemDVOut),
        remainingOrderAttachmentsOut=int(row.ONRemAtOut),
    )
    
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
    
def convert_HTC300_G000_T030_Co_Info_Chg_History(conn : Connection, row):
    userId = getUserIdFromUsername(conn, row.CoInfo_LID)
    addCompanyChangeHistory(
        conn,
        companyId=row.CoInfo_CoID,
        userId=userId,
        dateChanged=row.CoInfo_Now,
        changes=row.CoInfo_Chgs
    )
    
def convert_HTC300_G000_T040_Branch_Info_Chg_History(conn : Connection, row):
    userId = getUserIdFromUsername(conn, row.BrInfo_LID)
    addBranchChangeHistory(
        conn,
        branchId=row.BrInfo_BrID,
        userId=userId,
        dateChanged=row.BrInfo_Now,
        changes=row.BrInfo_Chgs
    )
    

def convert_HTC300_G010_T010_DFW_ACI_Data(conn : Connection, row):
    cityId, postalCodeId = addCityPostalCode(
        conn,
        cityName=row.CITY_PLACE,
        postalCode=row.ZIP_CODE,
        regionDetails={'isoCode' : row.STATE},
        countryDetails={'countryName' : row.Country}
    )
    
    if not cityId or not postalCodeId:
        return
    
    if row.AREA.strip().upper() == 'HOTSHOT':
        correctArea = '@'
    elif row.AREA.strip() == '':
        correctArea = None
    else:
        correctArea = row.AREA.strip().lower()
    
    addAciData(
        conn,
        aciDataId=row.ID,
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
    

def convert_HTC300_G010_T030_ACI_Update_History(conn : Connection, row):
    userId = conn.sqlGetInfo('user', 'id', f"[username] = '{row.ACI_UpdtLID}'")
    if not userId:
        userId = 0
    else:
        userId = userId[0].id
        
    addAciDataChangeHistory(
        conn,
        aciDataId=row.ACI_LineNbr,
        userId=userId,
        dateChanged=row.ACI_UpdtDate,
        changes=row.ACI_Updates
    )
    
def convert_HTC300_G020_T010_Status_Values(conn : Connection, row):
    addOrderStatus(
      conn, 
      orderStatusId=row.Stat_Seq,
      sequenceNumber=row.Stat_Seq,
      orderStatusName=row.Stat_Text,
      branchId=row.Stat_BrID,
      isOnManifest=row.OnManifest,
      isSetToAutoNotify=row.AutoNotify,
      isActive=row.Stat_Active
    )
    
def convert_HTC300_G020_T030_Status_Update_History(conn : Connection, row):
    addOrderStatusChangeHistory(
        conn,
        dateChanged=row.STAT_UpdtDate,
        orderStatusId=row.STAT_Seq,
        userId=getUserIdFromUsername(conn, row.STAT_UpdtLID), 
        changes=row.STAT_Changes if not row.STAT_Changes.strip() == '' else 'N/A'
    )
    

def convert_HTC300_G025_T025_Positions_Change_History(conn : Connection, row):
    addPositionChangeHistory(
        conn,
        dateChanged=row.PosnHist_Date,
        positionId=row.PosnHist_ID,
        userId=getUserIdFromUsername(conn, row.PosnHist_ChgdBy), 
        changes=row.PosnHist_Changes.strip() if not row.PosnHist_Changes.strip() == '' else 'N/A'
    )
    
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
    
def convert_HTC300_G030_T030_Customer_Update_History(conn : Connection, row):
    if row.Cust_CoID == 1 and row.Cust_BrID == 1:
      addCustomerChangeHistory(
          conn,
          dateChanged=combineDateTime(row.Cust_UpdtDate, row.Cust_UpdtTime),
          customerId=row.Cust_CustomerID,
          userId=getUserIdFromUsername(conn, row.Cust_UpdtLID), 
          changes=row.Cust_FldUpdts.strip() if not row.Cust_FldUpdts.strip() == '' else 'N/A'
      )
      
def convert_HTC300_G040_T010A_Open_Orders(conn: Connection, row):
    # Retrieve rate ID based on the tariff
    rateId = 1
    # Add the order
    addOrder(
        conn,
        orderId=row.M_OrderNo,
        branchId=row.M_BrID,
        orderTypeId=row.M_OrderType,
        customerId=row.M_CustomerID,
        agentId=row.M_CustAgent if row.M_CustAgent else None,
        rateId=rateId,
        hawb=row.M_HAWB,
        mawb=row.M_MAWB,
        orderNotes=row.M_OrderNotes,
        puTimeStart=combineDateTime(row.M_PUDate, row.M_PUTimeStart),
        puTimeEnd=combineDateTime(row.M_PUDate, row.M_PUTimeEnd),
        delTimeStart=combineDateTime(row.M_DelDate, row.M_DelTimeStart),
        delTimeEnd=combineDateTime(row.M_DelDate, row.M_DelTimeEnd),
        puLocationId=row.M_PUID,
        puNotes=row.M_PUNotes,
        delLocationId=row.M_DelID,
        delNotes=row.M_DelNotes,
        driverName=row.M_Driver.strip(),
        podSignee=row.M_PODSig,
        podTimeSigned=combineDateTime(row.M_PODDate, row.M_PODTime),
        podNotes=row.M_PODNotes,
        statusId=row.m_StatSeq,
        ratingWeightCharges=row.M_Rate,
        ratingFuelCharges=row.M_FSC,
        ratingServiceCharges=row.M_Services,
        ratingTotalCharges=row.M_Charges,
        ratingTotalExpenses=row.M_Costs,
        ratingStorageCharges=row.M_StorageChgs,
        ratingAdjustments=row.M_Adjustments,
        ratingNotes=row.M_RatingNotes,
        quickbooksCustomerListId=row.M_QBCustomerListID,
        quickbooksCustomerName=row.M_QBCustFullName,
        quickbooksInvoiceReferenceNumber=row.M_QBInvoiceRefNumber,
        quickbooksLineSequenceNumber=row.M_QBInvoiceLineSeqNo,
        isAutoAssessorials=row.M_AutoAssessYN,
        isWeightChargeCalculated=row.M_WgtChgsCalcYN
    )
    
def convert_HTC300_G040_T010B_Invoiced_Orders(conn : Connection, row):
    # Retrieve rate ID based on the tariff
    rateId = 1
    # Add the order
    addOrder(
        conn,
        orderId=row.M_OrderNo,
        branchId=row.M_BrID,
        orderTypeId=row.M_OrderType,
        customerId=row.M_CustomerID,
        agentId=row.M_CustAgent if row.M_CustAgent else None,
        rateId=rateId,
        hawb=row.M_HAWB,
        mawb=row.M_MAWB,
        orderNotes=row.M_OrderNotes,
        puTimeStart=combineDateTime(row.M_PUDate, row.M_PUTimeStart),
        puTimeEnd=combineDateTime(row.M_PUDate, row.M_PUTimeEnd),
        delTimeStart=combineDateTime(row.M_DelDate, row.M_DelTimeStart),
        delTimeEnd=combineDateTime(row.M_DelDate, row.M_DelTimeEnd),
        puLocationId=row.M_PUID,
        puNotes=row.M_PUNotes,
        delLocationId=row.M_DelID,
        delNotes=row.M_DelNotes,
        driverName=row.M_Driver.strip(),
        podSignee=row.M_PODSig,
        podTimeSigned=combineDateTime(row.M_PODDate, row.M_PODTime),
        podNotes=row.M_PODNotes,
        statusId=row.m_StatSeq,
        ratingWeightCharges=row.M_Rate,
        ratingFuelCharges=row.M_FSC,
        ratingServiceCharges=row.M_Services,
        ratingTotalCharges=row.M_Charges,
        ratingTotalExpenses=row.M_Costs,
        ratingStorageCharges=row.M_StorageChgs,
        ratingAdjustments=row.M_Adjustments,
        ratingNotes=row.M_RatingNotes,
        quickbooksCustomerListId=row.M_QBCustomerListID,
        quickbooksCustomerName=row.M_QBCustFullName,
        quickbooksInvoiceReferenceNumber=row.M_QBInvoiceRefNumber,
        quickbooksLineSequenceNumber=row.M_QBInvoiceLineSeqNo,
        isAutoAssessorials=row.M_AutoAssessYN,
        isWeightChargeCalculated=row.M_WgtChgsCalcYN
    )
    
def convert_HTC300_G040_T010C_Remaining_Orders(conn : Connection, row):
    # Retrieve rate ID based on the tariff
    rateId = 1
    # Add the order
    addOrder(
        conn,
        orderId=row.M_OrderNo,
        branchId=row.M_BrID,
        orderTypeId=row.M_OrderType,
        customerId=row.M_CustomerID,
        agentId=row.M_CustAgent if row.M_CustAgent else None,
        rateId=rateId,
        hawb=row.M_HAWB,
        mawb=row.M_MAWB,
        orderNotes=row.M_OrderNotes,
        puTimeStart=combineDateTime(row.M_PUDate, row.M_PUTimeStart),
        puTimeEnd=combineDateTime(row.M_PUDate, row.M_PUTimeEnd),
        delTimeStart=combineDateTime(row.M_DelDate, row.M_DelTimeStart),
        delTimeEnd=combineDateTime(row.M_DelDate, row.M_DelTimeEnd),
        puLocationId=row.M_PUID,
        puNotes=row.M_PUNotes,
        delLocationId=row.M_DelID,
        delNotes=row.M_DelNotes,
        driverName=row.M_Driver.strip(),
        podSignee=row.M_PODSig,
        podTimeSigned=combineDateTime(row.M_PODDate, row.M_PODTime),
        podNotes=row.M_PODNotes,
        statusId=row.m_StatSeq,
        ratingWeightCharges=row.M_Rate,
        ratingFuelCharges=row.M_FSC,
        ratingServiceCharges=row.M_Services,
        ratingTotalCharges=row.M_Charges,
        ratingTotalExpenses=row.M_Costs,
        ratingStorageCharges=row.M_StorageChgs,
        ratingAdjustments=row.M_Adjustments,
        ratingNotes=row.M_RatingNotes,
        quickbooksCustomerListId=row.M_QBCustomerListID,
        quickbooksCustomerName=row.M_QBCustFullName,
        quickbooksInvoiceReferenceNumber=row.M_QBInvoiceRefNumber,
        quickbooksLineSequenceNumber=row.M_QBInvoiceLineSeqNo,
        isAutoAssessorials=row.M_AutoAssessYN,
        isWeightChargeCalculated=row.M_WgtChgsCalcYN
    )
    
def convert_HTC300_G040_T010D_Dock_Orders(conn : Connection, row):
    # Retrieve rate ID based on the tariff
    rateId = 1
    # Add the order
    
    if row.M_Driver:
        driverName = row.M_Driver.strip()
    else:
        driverName = None
    
    addOrder(
        conn,
        orderId=row.M_OrderNo,
        branchId=row.M_BrID,
        orderTypeId=row.M_OrderType,
        customerId=row.M_CustomerID,
        agentId=row.M_CustAgent if row.M_CustAgent else None,
        rateId=rateId,
        hawb=row.M_HAWB,
        mawb=row.M_MAWB,
        orderNotes=row.M_OrderNotes,
        puTimeStart=combineDateTime(row.M_PUDate, row.M_PUTimeStart),
        puTimeEnd=combineDateTime(row.M_PUDate, row.M_PUTimeEnd),
        delTimeStart=combineDateTime(row.M_DelDate, row.M_DelTimeStart),
        delTimeEnd=combineDateTime(row.M_DelDate, row.M_DelTimeEnd),
        puLocationId=row.M_PUID,
        puNotes=row.M_PUNotes,
        delLocationId=row.M_DelID,
        delNotes=row.M_DelNotes,
        driverName=driverName,
        podSignee=row.M_PODSig,
        podTimeSigned=combineDateTime(row.M_PODDate, row.M_PODTime),
        podNotes=row.M_PODNotes,
        statusId=row.m_StatSeq,
        ratingWeightCharges=row.M_Rate,
        ratingFuelCharges=row.M_FSC,
        ratingServiceCharges=row.M_Services,
        ratingTotalCharges=row.M_Charges,
        ratingTotalExpenses=row.M_Costs,
        ratingStorageCharges=row.M_StorageChgs,
        ratingAdjustments=row.M_Adjustments,
        ratingNotes=row.M_RatingNotes,
        quickbooksCustomerListId=row.M_QBCustomerListID,
        quickbooksCustomerName=row.M_QBCustFullName,
        quickbooksInvoiceReferenceNumber=row.M_QBInvoiceRefNumber,
        quickbooksLineSequenceNumber=row.M_QBInvoiceLineSeqNo,
        isAutoAssessorials=row.M_AutoAssessYN,
        isWeightChargeCalculated=row.M_WgtChgsCalcYN
    )
    
def convert_HTC300_G040_T010E_Service_Orders(conn : Connection, row):
    # Retrieve rate ID based on the tariff
    rateId = 1
    # Add the order
    addOrder(
        conn,
        orderId=row.M_OrderNo,
        branchId=row.M_BrID,
        orderTypeId=row.M_OrderType,
        customerId=row.M_CustomerID,
        agentId=row.M_CustAgent if row.M_CustAgent else None,
        rateId=rateId,
        hawb=row.M_HAWB,
        mawb=row.M_MAWB,
        orderNotes=row.M_OrderNotes,
        puTimeStart=combineDateTime(row.M_PUDate, row.M_PUTimeStart),
        puTimeEnd=combineDateTime(row.M_PUDate, row.M_PUTimeEnd),
        delTimeStart=combineDateTime(row.M_DelDate, row.M_DelTimeStart),
        delTimeEnd=combineDateTime(row.M_DelDate, row.M_DelTimeEnd),
        puLocationId=row.M_PUID,
        puNotes=row.M_PUNotes,
        delLocationId=row.M_DelID,
        delNotes=row.M_DelNotes,
        driverName=row.M_Driver.strip(),
        podSignee=row.M_PODSig,
        podTimeSigned=combineDateTime(row.M_PODDate, row.M_PODTime),
        podNotes=row.M_PODNotes,
        statusId=row.m_StatSeq,
        ratingWeightCharges=row.M_Rate,
        ratingFuelCharges=row.M_FSC,
        ratingServiceCharges=row.M_Services,
        ratingTotalCharges=row.M_Charges,
        ratingTotalExpenses=row.M_Costs,
        ratingStorageCharges=row.M_StorageChgs,
        ratingAdjustments=row.M_Adjustments,
        ratingNotes=row.M_RatingNotes,
        quickbooksCustomerListId=row.M_QBCustomerListID,
        quickbooksCustomerName=row.M_QBCustFullName,
        quickbooksInvoiceReferenceNumber=row.M_QBInvoiceRefNumber,
        quickbooksLineSequenceNumber=row.M_QBInvoiceLineSeqNo,
        isAutoAssessorials=row.M_AutoAssessYN,
        isWeightChargeCalculated=row.M_WgtChgsCalcYN
    )
    
def convert_HTC300_G040_T011A_Open_Order_Assessorials(conn : Connection, row):
    if row.OA_MinutesWaitTime:
        basisCount = row.OA_MinutesWaitTime
    elif row.OA_HowManyMiles:
        basisCount = row.OA_HowManyMiles
    elif row.OA_HowManyHrs:
        basisCount = row.OA_HowManyHrs
    else:
        basisCount = None
  
    addOrderAssessorial(
        conn,
        orderId=row.OA_OrderNo,
        parentType=row.OA_AssParent,
        assessorialId=row.OA_AssID,
        basisCount=basisCount,
        totalCharge=row.OA_TotalCharges
    )
    
def convert_HTC300_G040_T011B_Invoiced_Order_Assessorials(conn : Connection, row):
    if row.OA_MinutesWaitTime:
        basisCount = row.OA_MinutesWaitTime
    elif row.OA_HowManyMiles:
        basisCount = row.OA_HowManyMiles
    elif row.OA_HowManyHrs:
        basisCount = row.OA_HowManyHrs
    else:
        basisCount = None
  
    addOrderAssessorial(
        conn,
        orderId=row.OA_OrderNo,
        parentType=row.OA_AssParent,
        assessorialId=row.OA_AssID,
        basisCount=basisCount,
        totalCharge=row.OA_TotalCharges
    )
    

def convert_HTC300_G040_T011C_Remaining_Order_Assessorials(conn : Connection, row):
    if row.OA_MinutesWaitTime:
        basisCount = row.OA_MinutesWaitTime
    elif row.OA_HowManyMiles:
        basisCount = row.OA_HowManyMiles
    elif row.OA_HowManyHrs:
        basisCount = row.OA_HowManyHrs
    else:
        basisCount = None
  
    addOrderAssessorial(
        conn,
        orderId=row.OA_OrderNo,
        parentType=row.OA_AssParent,
        assessorialId=row.OA_AssID,
        basisCount=basisCount,
        totalCharge=row.OA_TotalCharges
    )
    

def convert_HTC300_G040_T011D_Dock_Order_Assessorials(conn : Connection, row):
    if row.OA_MinutesWaitTime:
        basisCount = row.OA_MinutesWaitTime
    elif row.OA_HowManyMiles:
        basisCount = row.OA_HowManyMiles
    elif row.OA_HowManyHrs:
        basisCount = row.OA_HowManyHrs
    else:
        basisCount = None
  
    addOrderAssessorial(
        conn,
        orderId=row.OA_OrderNo,
        parentType=row.OA_AssParent,
        assessorialId=row.OA_AssID,
        basisCount=basisCount,
        totalCharge=row.OA_TotalCharges
    )
    
def convert_HTC300_G040_T011E_Service_Order_Assessorials(conn : Connection, row):
    if row.OA_MinutesWaitTime:
        basisCount = row.OA_MinutesWaitTime
    elif row.OA_HowManyMiles:
        basisCount = row.OA_HowManyMiles
    elif row.OA_HowManyHrs:
        basisCount = row.OA_HowManyHrs
    else:
        basisCount = None
  
    addOrderAssessorial(
        conn,
        orderId=row.OA_OrderNo,
        parentType=row.OA_AssParent,
        assessorialId=row.OA_AssID,
        basisCount=basisCount,
        totalCharge=row.OA_TotalCharges
    )
    
def convert_HTC300_G040_T012A_Open_Order_Dims(conn : Connection, row):
    addOrderDim(
        conn,
        orderId = row.OD_OrderNo,
        unitType=row.OD_UnitType,
        unitQuantity=row.OD_UnitQty,
        dimHeight=row.OD_UnitHeight,
        dimLength=row.OD_UnitLength,
        dimWidth=row.OD_UnitWidth,
        unitWeight=row.OD_UnitWeight,
        dimWeight=row.OD_UnitDimWeight,
    )
    
def convert_HTC300_G040_T012B_Invoiced_Order_Dims(conn : Connection, row):
    addOrderDim(
        conn,
        orderId = row.OD_OrderNo,
        unitType=row.OD_UnitType,
        unitQuantity=row.OD_UnitQty,
        dimHeight=row.OD_UnitHeight,
        dimLength=row.OD_UnitLength,
        dimWidth=row.OD_UnitWidth,
        unitWeight=row.OD_UnitWeight,
        dimWeight=row.OD_UnitDimWeight,
    )
    
def convert_HTC300_G040_T012C_Remaining_Order_Dims(conn : Connection, row):
    addOrderDim(
        conn,
        orderId = row.OD_OrderNo,
        unitType=row.OD_UnitType,
        unitQuantity=row.OD_UnitQty,
        dimHeight=row.OD_UnitHeight,
        dimLength=row.OD_UnitLength,
        dimWidth=row.OD_UnitWidth,
        unitWeight=row.OD_UnitWeight,
        dimWeight=row.OD_UnitDimWeight,
    )
    
def convert_HTC300_G040_T012D_Dock_Order_Dims(conn : Connection, row):
    addOrderDim(
        conn,
        orderId = row.OD_OrderNo,
        unitType=row.OD_UnitType,
        unitQuantity=row.OD_UnitQty,
        dimHeight=row.OD_UnitHeight,
        dimLength=row.OD_UnitLength,
        dimWidth=row.OD_UnitWidth,
        unitWeight=row.OD_UnitWeight,
        dimWeight=row.OD_UnitDimWeight,
    )
    
def convert_HTC300_G040_T012E_Service_Order_Dims(conn : Connection, row):
    addOrderDim(
        conn,
        orderId = row.OD_OrderNo,
        unitType=row.OD_UnitType,
        unitQuantity=row.OD_UnitQty,
        dimHeight=row.OD_UnitHeight,
        dimLength=row.OD_UnitLength,
        dimWidth=row.OD_UnitWidth,
        unitWeight=row.OD_UnitWeight,
        dimWeight=row.OD_UnitDimWeight,
    )
    
def convert_HTC300_G040_T013A_Open_Order_Drivers(conn : Connection, row):
    addOrderDriver(
      conn,
      orderId=row.ODvr_OrderNo,
      driverUserId=row.ODvr_EmpID,
      orderLeg=row.ODvr_Leg,
      driverRole=row.ODvr_Role
    )
    
def convert_HTC300_G040_T013B_Invoiced_Order_Drivers(conn : Connection, row):
    addOrderDriver(
      conn,
      orderId=row.ODvr_OrderNo,
      driverUserId=row.ODvr_EmpID,
      orderLeg=row.ODvr_Leg,
      driverRole=row.ODvr_Role
    )

def convert_HTC300_G040_T013C_Remaining_Order_Drivers(conn : Connection, row):
    addOrderDriver(
      conn,
      orderId=row.ODvr_OrderNo,
      driverUserId=row.ODvr_EmpID,
      orderLeg=row.ODvr_Leg,
      driverRole=row.ODvr_Role
    )
    
def convert_HTC300_G040_T013D_Dock_Order_Drivers(conn : Connection, row):
    addOrderDriver(
      conn,
      orderId=row.ODvr_OrderNo,
      driverUserId=row.ODvr_EmpID,
      orderLeg=row.ODvr_Leg,
      driverRole=row.ODvr_Role
    )
    
def convert_HTC300_G040_T013E_Service_Order_Drivers(conn : Connection, row):
    addOrderDriver(
      conn,
      orderId=row.ODvr_OrderNo,
      driverUserId=row.ODvr_EmpID,
      orderLeg=row.ODvr_Leg,
      driverRole=row.ODvr_Role
    )
    
def convert_HTC300_G040_T014A_Open_Order_Attachments(conn : Connection, row):
    addOrderAttachment(
      conn,
      orderId=row.Att_OrderNo,
      attachmentPath=row.Att_Path,
      fileSize=row.ATT_Size
    )
    
def convert_HTC300_G040_T014B_Invoiced_Order_Attachments(conn : Connection, row):
    addOrderAttachment(
      conn,
      orderId=row.Att_OrderNo,
      attachmentPath=row.Att_Path,
      fileSize=row.ATT_Size
    )
    
def convert_HTC300_G040_T014C_Remaining_Order_Attachments(conn : Connection, row):
    addOrderAttachment(
      conn,
      orderId=row.Att_OrderNo,
      attachmentPath=row.Att_Path,
      fileSize=row.ATT_Size
    )
    
def convert_HTC300_G040_T014D_Dock_Order_Attachments(conn : Connection, row):
    addOrderAttachment(
      conn,
      orderId=row.Att_OrderNo,
      attachmentPath=row.Att_Path,
      fileSize=row.Att_Size
    )
    
def convert_HTC300_G040_T014E_Service_Order_Attachments(conn : Connection, row):
    addOrderAttachment(
      conn,
      orderId=row.Att_OrderNo,
      attachmentPath=row.Att_Path,
      fileSize=row.Att_Size
    )
    
def convert_HTC300_G040_T030_Orders_Update_History(conn : Connection, row):
    if not row.Orders_OrderNbr:
        return
    addOrderChangeHistory(
        conn,
        orderId=row.Orders_OrderNbr,
        userId=getUserIdFromUsername(conn, row.Orders_UpdtLID),
        dateChanged=row.Orders_UpdtDate,
        changes=row.Orders_Changes.strip() if not row.Orders_Changes.strip() == '' else 'N/A'
    )
    
def convert_HTC300_G050_T010_Accessorials(conn : Connection, row):
    if row.AccType.lower() == 'asrl':
        if row.AccBasis.lower() == 'lb':
            basisType = 'weight'
        elif row.AccBasis.lower() == 'fxd':
            basisType = 'fixed'
        elif row.AccBasis.lower() == 'ask':
            basisType = 'prompt'
            
        addAssessorial(
            conn,
            branchId=row.AccBrID,
            assessorialId=row.AccID,
            assessorialName=row.AccDesc,
            isActive=row.AccActive,
            minCharge=row.AccMinCharge,
            basisType=basisType,
            userPrompt=row.Acc_Question,
            basisPortion=row.AccPortion,
            basisRate=row.AccRate,
            dateCreated=row.Acc_DateAdded,
            notes=row.Acc_Comments
        )
'''    elif row.AccType.lower() == 'spcl':
        addSpecial(
            conn,
            branchId=row.AccBrID,
            oldId=row.AccID,
            weekday=,
            startTime=0,
            endTime=0,
            area='A',
            isActive=row.AccActive,
            amountCharged
        )'''
        
def convert_HTC300_G050_T030_Accessorials_Update_History(conn : Connection, row):
    assessorialType = conn.accessGetTableInfo('htc300', 'HTC300_G050_T010 Accessorials', 'AccType', whereDetails={'AccID': row.Acc_AccID})[0].AccType
    
    if assessorialType.lower() == 'asrl':
        addAssessorialChangeHistory(
            conn,
            assessorialId=row.Acc_AccID,
            userId=getUserIdFromUsername(conn, row.Acc_UpdtLID),
            dateChanged=row.Acc_UpdtDate,
            changes=row.Acc_Changes.strip() if not row.Acc_Changes.strip() == '' else 'N/A'
        )
    elif assessorialType.lower() == 'spcl':
        addSpecialChangeHistory(
            conn,
            specialId=row.Acc_AccID,
            userId=getUserIdFromUsername(conn, row.Acc_UpdtLID),
            dateChanged=row.Acc_UpdtDate,
            changes=row.Acc_Changes.strip() if not row.Acc_Changes.strip() == '' else 'N/A'
        )
        
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
    
def convert_HTC300_G060_T030_Addresses_Update_History(conn : Connection, row):
    addLocationChangeHistory(
        conn,
        locationId=row.Addr_ID,
        userId=getUserIdFromUsername(conn, row.Addr_UpdtLID),
        dateChanged=row.Addr_UpdtDate,
        changes=row.Addr_Chgs.strip() if not row.Addr_Chgs.strip() == '' else 'N/A'
    )
    
def convert_HTC300_G070_T010_Rates(conn : Connection):
    rate_areaInfo = conn.accessGetTableInfo('htc300', 'HTC300_G070_T010 Rates')
    for row in rate_areaInfo:
        pass
    print('Completed [HTC300_G070_T010 Rates] Conversion.')

def convert_HTC300_G070_T030_Rates_Update_History(conn : Connection):
    rate_change_historyInfo = conn.accessGetTableInfo('htc300', 'HTC300_G070_T030 Rates Update History')
    for row in rate_change_historyInfo:
        pass
    print('Completed [HTC300_G070_T030 Rates Update History] Conversion.')
    
def convert_HTC300_G080_T010_Agents(conn : Connection):
    agentInfo = conn.accessGetTableInfo('htc300', 'HTC300_G080_T010 Agents')
    for row in agentInfo:
        pass
    print('Completed [HTC300_G080_T010 Agents] Conversion.')
    
def convert_HTC300_G080_T020_Agent_Certifications(conn : Connection):
    agent_certificationInfo = conn.accessGetTableInfo('htc300', 'HTC300_G080_T020 Agent Certifications')
    for row in agent_certificationInfo:
        pass
    print('Completed [HTC300_G080_T020 Agent Certifications] Conversion.')    
    
def convert_HTC300_G080_T030_Agents_Change_History(conn : Connection):
    agent_change_historyInfo = conn.accessGetTableInfo('htc300', 'HTC300_G080_T030 Agents Change History')
    for row in agent_change_historyInfo:
        pass
    print('Completed [HTC300_G080_T030 Agents Change History] Conversion.')
    
def convert_HTC300_G090_T030_Staff_Chg_History(conn : Connection):
    user_change_historyInfo = conn.accessGetTableInfo('htc300', 'HTC300_G090_T030 Staff Chg History')
    for row in user_change_historyInfo:
        pass
    print('Completed [HTC300_G090_T030 Staff Chg History] Conversion.') 
    
def convert_HTC300_G100_T020_Certification_Trainers(conn : Connection):
    certification_test_trainerInfo = conn.accessGetTableInfo('htc300', 'HTC300_G100_T020 Certification Trainers')
    for row in certification_test_trainerInfo:
        pass
    print('Completed [HTC300_G100_T020 Certification Trainers] Conversion.')    

def convert_HTC300_G100_T021_Certifaction_Trainer_Change_History(conn : Connection):
    certification_trainer_change_historyInfo = conn.accessGetTableInfo('htc300', 'HTC300_G100_T021 Certifaction Trainer Change History')
    for row in certification_trainer_change_historyInfo:
        pass
    print('Completed [HTC300_G100_T021 Certifaction Trainer Change History] Conversion.')    

def convert_HTC300_G100_T030_CertificationTestCatalogChgHistory(conn : Connection):
    certification_test_change_historyInfo = conn.accessGetTableInfo('htc300', 'HTC300_G100_T030 CertificationTestCatalogChgHistory')
    for row in certification_test_change_historyInfo:
        pass
    print('Completed [HTC300_G100_T030 CertificationTestCatalogChgHistory] Conversion.')    
    
def convert_HTC400_G040_T010A_Orders(conn : Connection, row):
    rateId = 1    
    
    if row.M_Driver:
        driverName = row.M_Driver.strip()
    else:
        driverName = None
        
    addOrder(
        conn,
        orderId=row.M_OrderNo,
        branchId=row.M_BrID,
        orderTypeId=row.M_OrderType,
        customerId=row.M_CustomerID,
        agentId=row.M_CustAgent if row.M_CustAgent else None,
        rateId=rateId,
        hawb=row.M_HAWB,
        mawb=row.M_MAWB,
        orderNotes=row.M_OrderNotes,
        puTimeStart=combineDateTime(row.M_PUDate, row.M_PUTimeStart),
        puTimeEnd=combineDateTime(row.M_PUDate, row.M_PUTimeEnd),
        delTimeStart=combineDateTime(row.M_DelDate, row.M_DelTimeStart),
        delTimeEnd=combineDateTime(row.M_DelDate, row.M_DelTimeEnd),
        puLocationId=row.M_PUID,
        puNotes=row.M_PUNotes,
        delLocationId=row.M_DelID,
        delNotes=row.M_DelNotes,
        driverName=driverName,
        podSignee=row.M_PODSig,
        podTimeSigned=combineDateTime(row.M_PODDate, row.M_PODTime),
        podNotes=row.M_PODNotes,
        statusId=row.M_StatSeq,
        ratingWeightCharges=row.M_Rate,
        ratingFuelCharges=row.M_FSC,
        ratingServiceCharges=row.M_Services,
        ratingTotalCharges=row.M_Charges,
        ratingTotalExpenses=row.M_Costs,
        ratingStorageCharges=row.M_StorageChgs,
        ratingAdjustments=row.M_Adjustments,
        ratingNotes=row.M_RatingNotes,
        quickbooksCustomerListId=row.M_QBCustomerListID,
        quickbooksCustomerName=row.M_QBCustFullName,
        quickbooksInvoiceReferenceNumber=row.M_QBInvoiceRefNumber,
        quickbooksLineSequenceNumber=row.M_QBInvoiceLineSeqNo,
        isAutoAssessorials=row.M_AutoAssessYN,
        isWeightChargeCalculated=row.M_WgtChgsCalcYN
    )
  
def convert_HTC400_G040_T011A_Assessorials(conn : Connection, row):
    if row.OA_MinutesWaitTime:
        basisCount = row.OA_MinutesWaitTime
    elif row.OA_HowManyMiles:
        basisCount = row.OA_HowManyMiles
    elif row.OA_HowManyHrs:
        basisCount = row.OA_HowManyHrs
    else:
        basisCount = None
  
    addOrderAssessorial(
        conn,
        orderId=row.OA_OrderNo,
        parentType=row.OA_AssParent,
        assessorialId=row.OA_AssID,
        basisCount=basisCount,
        totalCharge=row.OA_TotalCharges
    )
    
def convert_HTC400_G040_T012A_Dims(conn : Connection, row):
    addOrderDim(
        conn,
        orderId = row.OD_OrderNo,
        unitType=row.OD_UnitType,
        unitQuantity=row.OD_UnitQty,
        dimHeight=row.OD_UnitHeight,
        dimLength=row.OD_UnitLength,
        dimWidth=row.OD_UnitWidth,
        unitWeight=row.OD_UnitWeight,
        dimWeight=row.OD_UnitDimWeight,
    )
    

def convert_HTC400_G040_T013A_Drivers(conn : Connection, row):
    addOrderDriver(
      conn,
      orderId=row.ODvr_OrderNo,
      driverUserId=row.ODvr_EmpID,
      orderLeg=row.ODvr_Leg,
      driverRole=row.ODvr_Role
    )
    
def convert_HTC400_G040_T014A_Attachments(conn : Connection, row):
    addOrderAttachment(
      conn,
      orderId=row.Att_OrderNo,
      attachmentPath=row.Att_Path,
      fileSize=row.Att_Size
    )
    
def convert_HTC400_G900_T010_Archive_Event_Log(conn : Connection):
    archive_error_logInfo = conn.accessGetTableInfo('htc400', 'HTC400_G900_T010 Archive Event Log')
    for row in archive_error_logInfo:
        pass
    print('Completed [HTC400_G900_T010 Archive Event Log] Conversion.')
    
