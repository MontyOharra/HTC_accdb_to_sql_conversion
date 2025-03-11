from typing import Any, Protocol, Callable
from .addDataFunctionDefinitions import *
from src.classes.SqlServerConn import SqlServerConn
from src.types import PyODBCRow

from src.utils.helpers import generatePasswordHash, generatePasswordSalt


def safeLower(value: Any) -> Any:
    """Converts value to lowercase if it's a string, otherwise returns the original value"""
    return value.lower() if isinstance(value, str) else value


def convert_HTC000_G010_T010_Company_Info(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    phoneId = addPhone(
        sqlConn,
        countryCode="1",
        areaCode=getPhoneAreaCode(row.CoOfcrPhone),
        phoneNumber=getPhoneNumber(row.CoOfcrPhone),
        phoneExtension=row.CoOfcrExtension,
    )
    faxId = addFax(
        sqlConn,
        countryCode="1",
        areaCode=getPhoneAreaCode(row.CoFax),
        faxNumber=getPhoneNumber(row.CoFax),
        faxExtension="",
    )

    addressId = addAddress(
        sqlConn,
        addressLine1=row.CoMailAddrLn1,
        addressLine2=row.CoMailAddrLn2,
        cityName=row.CoMailCity,
        postalCode=correctPostalCode(row.CoMailZip),
        regionDetails={"isoCode": row.CoMailState},
        countryDetails={"default": ""},
    )

    addCompany(
        sqlConn,
        companyId=row.CoID,
        companyName=safeLower(row.CoName),
        isActive=row.CoActive,
        scac=safeLower(row.CoSCAC),
        employerIdentificationNo=row.CoTaxID,
        website=safeLower(row.CoWebPage),
        isTsaCompliant=row.CoTSACompliant,
        airportCode=safeLower(row.CoAirportCode),
        cartageAgentType=row.CoCartageAgentType,
        logoPath=safeLower(row.CoLogo),
        addressId=addressId,
        phoneId=phoneId,
        faxId=faxId,
        email=safeLower(row.CoOfcrEmail),
        notes=row.CoNotes,
    )


def convert_HTC000_G025_T010_Positions(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    addPosition(
        sqlConn,
        positionId=row.Posn_ID,
        positionName=safeLower(row.Posn_Title),
        securityLevel=row.Posn_SecurityLevel,
        isActive=row.Posn_Status,
        branchId=row.Posn_BrID,
    )


def convert_HTC000_G090_T010_Staff(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    phoneMainId = addPhone(
        sqlConn,
        "1",
        getPhoneAreaCode(row.Staff_Phone),
        getPhoneNumber(row.Staff_Phone),
        "",
    )
    phoneMobileId = addPhone(
        sqlConn,
        "1",
        getPhoneAreaCode(row.Staff_Mobile),
        getPhoneNumber(row.Staff_Mobile),
        "",
    )
    phoneHomeId = addPhone(
        sqlConn,
        "1",
        getPhoneAreaCode(row.Staff_Home_Phone),
        getPhoneNumber(row.Staff_Home_Phone),
        "",
    )
    addressId = addAddress(
        sqlConn,
        safeLower(row.Staff_Home_Street1),
        safeLower(row.Staff_Home_Street2),
        safeLower(row.Staff_Home_City),
        safeLower(correctPostalCode(row.Staff_Home_Zip)),
        {"isoCode": safeLower(row.Staff_Home_StAbbr)},
        {"isoCode3": safeLower(row.Staff_Home_Country)},
    )

    if row.Staff_Password == None:
        passwordHash = None
        passwordSalt = None
    elif row.Staff_Password.strip() == "":
        passwordHash = ""
        passwordSalt = ""
    else:
        passwordSalt = generatePasswordSalt(16)
        passwordHash = generatePasswordHash(row.Staff_Password.strip(), passwordSalt)

    addUser(
        sqlConn,
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
        isActive=row.Staff_Active,
    )


def convert_HTC010_G000_T000_OrderType_Values(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    addOrderType(sqlConn, orderTypeId=row.OrdType_ID, orderTypeName=row.OrdType_Title)


def convert_HTC010_G000_T000_US_Zip_Codes(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    if row.ZipCodeType == "MILITARY":
        return
    if row.State in [
        "AB",
        "BC",
        "MB",
        "NB",
        "NL",
        "NT",
        "NS",
        "NU",
        "ON",
        "PE",
        "QC",
        "SK",
        "YT",
    ]:
        addCityPostalCode(
            sqlConn,
            cityName=row.City,
            postalCode=row.Zipcode,
            regionDetails={"isoCode": row.State},
            countryDetails={"countryName": "Canada"},
        )
    else:
        addCityPostalCode(
            sqlConn,
            cityName=row.City,
            postalCode=row.Zipcode,
            regionDetails={"isoCode": row.State},
            countryDetails={"default": ""},
        )


def convert_HTC010_G100_T010_Certification_Test_Catalog(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    addCertificationTest(
        sqlConn,
        certificationTestId=row.TestID,
        certificationName=row.TestTitle,
        certificationTestTrainerId=row.TestTrainerID,
        isActive=row.TestStatus,
    )


def convert_HTC300_G000_T000_Archive_Update_History(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    addArchiveHistory(
        sqlConn,
        dateArchived=row.ArcCnt_Date,
        openOrders=int(row.ArcCnt_OpnOrd) if row.ArcCnt_OpnOrd != None else 0,
        openOrderAssessorials=(
            int(row.ArcCnt_OpnAss) if row.ArcCnt_OpnAss != None else 0
        ),
        openOrderDimensions=int(row.ArcCnt_OpnDim) if row.ArcCnt_OpnDim != None else 0,
        openOrderDrivers=int(row.ArcCnt_OpnDvr) if row.ArcCnt_OpnDvr != None else 0,
        openOrderAttachments=int(row.ArcCnt_OpnAtt) if row.ArcCnt_OpnAtt != None else 0,
        invoicedOrders=int(row.ArcCnt_InvOrd) if row.ArcCnt_InvOrd != None else 0,
        invoicedOrderAssessorials=(
            int(row.ArcCnt_InvAss) if row.ArcCnt_InvAss != None else 0
        ),
        invoicedOrderDimensions=(
            int(row.ArcCnt_InvDim) if row.ArcCnt_InvDim != None else 0
        ),
        invoicedOrderDrivers=int(row.ArcCnt_InvDvr) if row.ArcCnt_InvDvr != None else 0,
        invoicedOrderAttachments=(
            int(row.ArcCnt_InvATT) if row.ArcCnt_InvATT != None else 0
        ),
        remainingOrders=int(row.ArcCnt_RemOrd) if row.ArcCnt_RemOrd != None else 0,
        remainingOrderAssessorials=(
            int(row.ArcCnt_RemAss) if row.ArcCnt_RemAss != None else 0
        ),
        remainingOrderDimensions=(
            int(row.ArcCnt_RemDim) if row.ArcCnt_RemDim != None else 0
        ),
        remainingOrderDrivers=(
            int(row.ArcCnt_RemDvr) if row.ArcCnt_RemDvr != None else 0
        ),
        remainingOrderAttachments=(
            int(row.ArcCnt_RemATT) if row.ArcCnt_RemATT != None else 0
        ),
        dockOrders=int(row.ArcCnt_DckOrd) if row.ArcCnt_DckOrd != None else 0,
        dockOrderAssessorials=(
            int(row.ArcCnt_DckAss) if row.ArcCnt_DckAss != None else 0
        ),
        dockOrderDimensions=int(row.ArcCnt_DckDim) if row.ArcCnt_DckDim != None else 0,
        dockOrderDrivers=int(row.ArcCnt_DckDvr) if row.ArcCnt_DckDvr != None else 0,
        dockOrderAttachments=int(row.ArcCnt_DckATT) if row.ArcCnt_DckATT != None else 0,
        serviceOrders=int(row.ArcCnt_SvcOrd) if row.ArcCnt_SvcOrd != None else 0,
        serviceOrderAssessorials=(
            int(row.ArcCnt_SvcAss) if row.ArcCnt_SvcAss != None else 0
        ),
        serviceOrderDimensions=(
            int(row.ArcCnt_SvcDim) if row.ArcCnt_SvcDim != None else 0
        ),
        serviceOrderDrivers=int(row.ArcCnt_SvcDvr) if row.ArcCnt_SvcDvr != None else 0,
        serviceOrderAttachments=(
            int(row.ArcCnt_SvcATT) if row.ArcCnt_SvcATT != None else 0
        ),
        activeOrderHistory=(
            int(row.ArcCnt_ActiveHist) if row.ArcCnt_ActiveHist != None else 0
        ),
        activeOrderHawbs=(
            int(row.ArcCnt_ActiveHAWB) if row.ArcCnt_ActiveHAWB != None else 0
        ),
        archivedOrders=int(row.ArcCnt_ArcOrd) if row.ArcCnt_ArcOrd != None else 0,
        archivedOrderAssessorials=(
            int(row.ArcCnt_ArcAss) if row.ArcCnt_ArcAss != None else 0
        ),
        archivedOrderDimensions=(
            int(row.ArcCnt_ArcDim) if row.ArcCnt_ArcDim != None else 0
        ),
        archivedOrderDrivers=int(row.ArcCnt_ArcDvr) if row.ArcCnt_ArcDvr != None else 0,
        archivedOrderAttachments=(
            int(row.ArcCnt_ArcATT) if row.ArcCnt_ArcATT != None else 0
        ),
        archivedOrderHistory=(
            int(row.ArcCnt_AchiveHist) if row.ArcCnt_AchiveHist != None else 0
        ),
        archivedOrderHawbs=(
            int(row.ArcCnt_ArchiveHAWB) if row.ArcCnt_ArchiveHAWB != None else 0
        ),
        removedOrders=(
            int(row.ArcCnt_RmvdOrders) if row.ArcCnt_RmvdOrders != None else 0
        ),
        removedOrderAssessorials=(
            int(row.ArcCnt_RmvdAss) if row.ArcCnt_RmvdAss != None else 0
        ),
        removedOrderDimensions=(
            int(row.ArcCnt_RmvdDims) if row.ArcCnt_RmvdDims != None else 0
        ),
        removedOrderDrivers=(
            int(row.ArcCnt_RmvdDvrs) if row.ArcCnt_RmvdDvrs != None else 0
        ),
        removedOrderAttachments=(
            int(row.ArcCnt_RmvdAtts) if row.ArcCnt_RmvdAtts != None else 0
        ),
        removedOrderHistory=(
            int(row.ArcCnt_RmvdHist) if row.ArcCnt_RmvdHist != None else 0
        ),
        removedOrderHawbs=(
            int(row.ArcCnt_RmvdHAWB) if row.ArcCnt_RmvdHAWB != None else 0
        ),
    )


def convert_HTC300_G000_T000_Holidays(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    addHoliday(sqlConn, holidayName=row.HolidayName, holidayDate=row.HolidayDate)


def convert_HTC300_G000_T000_Over_Night_Update_History(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    userId = getUserIdFromUsername(sqlConn, row.ONUser)

    addOvernightMaintenanceHistory(
        sqlConn,
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


def convert_HTC300_G000_T020_Branch_Info(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    addressId = addAddress(
        sqlConn,
        row.BrAddrLn1,
        row.BrAddrLn2,
        row.BrCity,
        row.BrZip,
        {"isoCode": row.BrStOrProv},
        {"default": ""},
    )
    phoneId = addPhone(
        sqlConn,
        "1",
        getPhoneAreaCode(row.BrDispPhone),
        getPhoneNumber(row.BrDispPhone),
        row.BrDispExtension,
    )
    faxId = addFax(
        sqlConn,
        "1",
        getPhoneAreaCode(row.BrDispFax),
        getPhoneNumber(row.BrDispFax),
        row.BrDispExtension,
    )

    addBranch(
        sqlConn,
        branchId=row.BrID,
        branchName=row.BrName,
        companyId=row.BrCoID,
        airportCode=safeLower(row.BrAirportCode),
        isActive=row.BrActive,
        cartageAgentType=row.BrCartageAgentType,
        fuelServiceCharge=row.BrFSC,
        transferRate=row.BrTrnsfrRate,
        aciLow=safeLower(row.BrLowACI),
        aciHigh=safeLower(row.BrHighACI),
        addressId=addressId,
        phoneId=phoneId,
        faxId=faxId,
        email=safeLower(row.BrDispEmail),
        notes=row.BrNotes,
        internationalAirDimDivisor=row.BrDimFIntlAir,
        domesticAirDimDivisor=row.BrDimFNatlAir,
        truckDimDivisor=row.BrDimfTruck,
    )


def convert_HTC300_G000_T030_Co_Info_Chg_History(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    userId = getUserIdFromUsername(sqlConn, row.CoInfo_LID)
    addCompanyChangeHistory(
        sqlConn,
        companyId=row.CoInfo_CoID,
        userId=userId,
        dateChanged=row.CoInfo_Now,
        changes=row.CoInfo_Chgs,
    )


def convert_HTC300_G000_T040_Branch_Info_Chg_History(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    userId = getUserIdFromUsername(sqlConn, row.BrInfo_LID)
    addBranchChangeHistory(
        sqlConn,
        branchId=row.BrInfo_BrID,
        userId=userId,
        dateChanged=row.BrInfo_Now,
        changes=row.BrInfo_Chgs,
    )


def convert_HTC300_G010_T010_DFW_ACI_Data(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    cityId, postalCodeId = addCityPostalCode(
        sqlConn,
        cityName=safeLower(row.CITY_PLACE),
        postalCode=safeLower(row.ZIP_CODE),
        regionDetails={"isoCode": safeLower(row.STATE)},
        countryDetails={"countryName": safeLower(row.Country)},
    )

    if not cityId or not postalCodeId:
        return

    if row.AREA.strip().upper() == "HOTSHOT":
        correctArea = "@"
    elif row.AREA.strip() == "":
        correctArea = None
    else:
        correctArea = row.AREA.strip().lower()

    addAciData(
        sqlConn,
        aciDataId=row.ID,
        cityId=cityId,
        branchId=row.ACIBrID,
        postalCodeId=postalCodeId,
        airportCode=row.AIRP_CODE,
        carrier=row.CARRIER,
        area=safeLower(correctArea),
        rateMin=row.RATE_MIN,
        rate100=row.RATE_100,
        rate1000=row.RATE_1000,
        rate2000=row.RATE_2000,
        rate5000=row.RATE_5000,
        dateCreated=row.CreateDate,
        createdBy=getUserIdFromUsername(sqlConn, row.CreatedBy),
        isActive=row.Active,
    )


def convert_HTC300_G010_T030_ACI_Update_History(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    userId = sqlConn.select("user", "id", f"[username] = '{row.ACI_UpdtLID}'")
    if not userId:
        userId = 0
    else:
        userId = userId[0].id

    addAciDataChangeHistory(
        sqlConn,
        aciDataId=row.ACI_LineNbr,
        userId=userId,
        dateChanged=row.ACI_UpdtDate,
        changes=row.ACI_Updates,
    )


def convert_HTC300_G020_T010_Status_Values(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    addOrderStatus(
        sqlConn,
        orderStatusId=row.Stat_Seq,
        sequenceNumber=row.Stat_Seq,
        orderStatusName=row.Stat_Text,
        branchId=row.Stat_BrID,
        isOnManifest=row.OnManifest,
        isSetToAutoNotify=row.AutoNotify,
        isActive=row.Stat_Active,
    )


def convert_HTC300_G020_T030_Status_Update_History(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    addOrderStatusChangeHistory(
        sqlConn,
        dateChanged=row.STAT_UpdtDate,
        orderStatusId=row.STAT_Seq if row.STAT_Seq else 0,
        userId=getUserIdFromUsername(sqlConn, row.STAT_UpdtLID),
        changes=(
            row.STAT_Changes.strip() if not row.STAT_Changes.strip() == "" else "N/A"
        ),
    )


def convert_HTC300_G025_T025_Positions_Change_History(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    addPositionChangeHistory(
        sqlConn,
        dateChanged=row.PosnHist_Date,
        positionId=row.PosnHist_ID,
        userId=getUserIdFromUsername(sqlConn, row.PosnHist_ChgdBy),
        changes=(
            row.PosnHist_Changes.strip()
            if not row.PosnHist_Changes.strip() == ""
            else "N/A"
        ),
    )


def convert_HTC300_G030_T010_Customers(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    cusAddrLine1 = row.Cus_AddrLn1.replace("\xa0", " ").strip().lower()
    cusAddrLine2 = row.Cus_AddrLn2.replace("\xa0", " ").strip().lower()
    cusCity = row.Cus_City.replace("\xa0", " ").replace("'", "''").strip().lower()
    cusZip = row.Cus_Zip.replace("\xa0", " ").strip().lower()
    cusState = row.Cus_State.replace("\xa0", " ").strip().lower()
    if row.Cus_Country == None:
        cusCountry = ""
    else:
        cusCountry = row.Cus_Country.replace("\xa0", " ").strip().lower()

    if cusCity == "mississuaga":
        addressId = addAddress(
            sqlConn,
            cusAddrLine1,
            cusAddrLine2,
            cusCity,
            cusZip,
            {"isoCode": "on"},
            {"isoCode2": "ca"},
        )
    else:
        if cusCountry == "":
            if cusState in ["on", "qc", "mb"]:
                addressId = addAddress(
                    sqlConn,
                    cusAddrLine1,
                    cusAddrLine2,
                    cusCity,
                    cusZip,
                    {"isoCode": cusState},
                    {"isoCode2": "ca"},
                )
            else:
                addressId = addAddress(
                    sqlConn,
                    cusAddrLine1,
                    cusAddrLine2,
                    cusCity,
                    cusZip,
                    regionDetails={"isoCode": cusState},
                    countryDetails={"default": ""},
                )
        elif cusCountry == "canada":
            addressId = addAddress(
                sqlConn,
                cusAddrLine1,
                cusAddrLine2,
                cusCity,
                cusZip,
                {"isoCode": cusState},
                {"isoCode2": "ca"},
            )
        else:
            addressId = addAddress(
                sqlConn,
                cusAddrLine1,
                cusAddrLine2,
                cusCity,
                cusZip,
                regionDetails={"isoCode": cusState},
                countryDetails={"default": ""},
            )

    phoneId = addPhone(
        sqlConn,
        "1",
        getPhoneAreaCode(row.Cus_Phone),
        getPhoneNumber(row.Cus_Phone),
        row.Cus_Extension,
    )

    for assessorialId in getAssessorialIds(row.Cus_Assessorials):
        addCustomerDefaultAssessorial(
            sqlConn, customerId=row.CustomerID, assessorialId=assessorialId
        )

    defaultRateId = 1
    addCustomer(
        sqlConn,
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


def convert_HTC300_G030_T030_Customer_Update_History(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    if row.Cust_CoID == 1 and row.Cust_BrID == 1:
        addCustomerChangeHistory(
            sqlConn,
            dateChanged=combineDateTime(row.Cust_UpdtDate, row.Cust_UpdtTime),
            customerId=row.Cust_CustomerID,
            userId=getUserIdFromUsername(sqlConn, row.Cust_UpdtLID),
            changes=(
                row.Cust_FldUpdts.strip()
                if not row.Cust_FldUpdts.strip() == ""
                else "N/A"
            ),
        )


def convert_HTC300_G040_T010A_Open_Orders(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    rateId = 1
    addOrder(
        sqlConn,
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
        isWeightChargeCalculated=row.M_WgtChgsCalcYN,
    )


def convert_HTC300_G040_T010B_Invoiced_Orders(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    rateId = 1
    addOrder(
        sqlConn,
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
        isWeightChargeCalculated=row.M_WgtChgsCalcYN,
    )


def convert_HTC300_G040_T010C_Remaining_Orders(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    rateId = 1
    addOrder(
        sqlConn,
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
        isWeightChargeCalculated=row.M_WgtChgsCalcYN,
    )


def convert_HTC300_G040_T010D_Dock_Orders(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    rateId = 1
    if row.M_Driver:
        driverName = row.M_Driver.strip()
    else:
        driverName = None

    addOrder(
        sqlConn,
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
        isWeightChargeCalculated=row.M_WgtChgsCalcYN,
    )


def convert_HTC300_G040_T010E_Service_Orders(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    rateId = 1
    addOrder(
        sqlConn,
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
        isWeightChargeCalculated=row.M_WgtChgsCalcYN,
    )


def convert_HTC300_G040_T011A_Open_Order_Assessorials(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    if row.OA_MinutesWaitTime:
        basisCount = row.OA_MinutesWaitTime
    elif row.OA_HowManyMiles:
        basisCount = row.OA_HowManyMiles
    elif row.OA_HowManyHrs:
        basisCount = row.OA_HowManyHrs
    else:
        basisCount = None

    addOrderAssessorial(
        sqlConn,
        orderId=row.OA_OrderNo,
        parentType=row.OA_AssParent,
        assessorialId=row.OA_AssID,
        basisCount=basisCount,
        totalCharge=row.OA_TotalCharges,
    )


def convert_HTC300_G040_T011B_Invoiced_Order_Assessorials(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    if row.OA_MinutesWaitTime:
        basisCount = row.OA_MinutesWaitTime
    elif row.OA_HowManyMiles:
        basisCount = row.OA_HowManyMiles
    elif row.OA_HowManyHrs:
        basisCount = row.OA_HowManyHrs
    else:
        basisCount = None

    addOrderAssessorial(
        sqlConn,
        orderId=row.OA_OrderNo,
        parentType=row.OA_AssParent,
        assessorialId=row.OA_AssID,
        basisCount=basisCount,
        totalCharge=row.OA_TotalCharges,
    )


def convert_HTC300_G040_T011C_Remaining_Order_Assessorials(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    if row.OA_MinutesWaitTime:
        basisCount = row.OA_MinutesWaitTime
    elif row.OA_HowManyMiles:
        basisCount = row.OA_HowManyMiles
    elif row.OA_HowManyHrs:
        basisCount = row.OA_HowManyHrs
    else:
        basisCount = None

    addOrderAssessorial(
        sqlConn,
        orderId=row.OA_OrderNo,
        parentType=row.OA_AssParent,
        assessorialId=row.OA_AssID,
        basisCount=basisCount,
        totalCharge=row.OA_TotalCharges,
    )


def convert_HTC300_G040_T011D_Dock_Order_Assessorials(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    if row.OA_MinutesWaitTime:
        basisCount = row.OA_MinutesWaitTime
    elif row.OA_HowManyMiles:
        basisCount = row.OA_HowManyMiles
    elif row.OA_HowManyHrs:
        basisCount = row.OA_HowManyHrs
    else:
        basisCount = None

    addOrderAssessorial(
        sqlConn,
        orderId=row.OA_OrderNo,
        parentType=row.OA_AssParent,
        assessorialId=row.OA_AssID,
        basisCount=basisCount,
        totalCharge=row.OA_TotalCharges,
    )


def convert_HTC300_G040_T011E_Service_Order_Assessorials(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    if row.OA_MinutesWaitTime:
        basisCount = row.OA_MinutesWaitTime
    elif row.OA_HowManyMiles:
        basisCount = row.OA_HowManyMiles
    elif row.OA_HowManyHrs:
        basisCount = row.OA_HowManyHrs
    else:
        basisCount = None

    addOrderAssessorial(
        sqlConn,
        orderId=row.OA_OrderNo,
        parentType=row.OA_AssParent,
        assessorialId=row.OA_AssID,
        basisCount=basisCount,
        totalCharge=row.OA_TotalCharges,
    )


def convert_HTC300_G040_T012A_Open_Order_Dims(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    addOrderDim(
        sqlConn,
        orderId=row.OD_OrderNo,
        unitType=row.OD_UnitType,
        unitQuantity=row.OD_UnitQty,
        dimHeight=row.OD_UnitHeight,
        dimLength=row.OD_UnitLength,
        dimWidth=row.OD_UnitWidth,
        unitWeight=row.OD_UnitWeight,
        dimWeight=row.OD_UnitDimWeight,
    )


def convert_HTC300_G040_T012B_Invoiced_Order_Dims(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    addOrderDim(
        sqlConn,
        orderId=row.OD_OrderNo,
        unitType=row.OD_UnitType,
        unitQuantity=row.OD_UnitQty,
        dimHeight=row.OD_UnitHeight,
        dimLength=row.OD_UnitLength,
        dimWidth=row.OD_UnitWidth,
        unitWeight=row.OD_UnitWeight,
        dimWeight=row.OD_UnitDimWeight,
    )


def convert_HTC300_G040_T012C_Remaining_Order_Dims(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    addOrderDim(
        sqlConn,
        orderId=row.OD_OrderNo,
        unitType=row.OD_UnitType,
        unitQuantity=row.OD_UnitQty,
        dimHeight=row.OD_UnitHeight,
        dimLength=row.OD_UnitLength,
        dimWidth=row.OD_UnitWidth,
        unitWeight=row.OD_UnitWeight,
        dimWeight=row.OD_UnitDimWeight,
    )


def convert_HTC300_G040_T012D_Dock_Order_Dims(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    addOrderDim(
        sqlConn,
        orderId=row.OD_OrderNo,
        unitType=row.OD_UnitType,
        unitQuantity=row.OD_UnitQty,
        dimHeight=row.OD_UnitHeight,
        dimLength=row.OD_UnitLength,
        dimWidth=row.OD_UnitWidth,
        unitWeight=row.OD_UnitWeight,
        dimWeight=row.OD_UnitDimWeight,
    )


def convert_HTC300_G040_T012E_Service_Order_Dims(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    addOrderDim(
        sqlConn,
        orderId=row.OD_OrderNo,
        unitType=row.OD_UnitType,
        unitQuantity=row.OD_UnitQty,
        dimHeight=row.OD_UnitHeight,
        dimLength=row.OD_UnitLength,
        dimWidth=row.OD_UnitWidth,
        unitWeight=row.OD_UnitWeight,
        dimWeight=row.OD_UnitDimWeight,
    )


def convert_HTC300_G040_T013A_Open_Order_Drivers(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    addOrderDriver(
        sqlConn,
        orderId=row.ODvr_OrderNo,
        driverUserId=row.ODvr_EmpID,
        orderLeg=row.ODvr_Leg,
        driverRole=row.ODvr_Role,
    )


def convert_HTC300_G040_T013B_Invoiced_Order_Drivers(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    addOrderDriver(
        sqlConn,
        orderId=row.ODvr_OrderNo,
        driverUserId=row.ODvr_EmpID,
        orderLeg=row.ODvr_Leg,
        driverRole=row.ODvr_Role,
    )


def convert_HTC300_G040_T013C_Remaining_Order_Drivers(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    addOrderDriver(
        sqlConn,
        orderId=row.ODvr_OrderNo,
        driverUserId=row.ODvr_EmpID,
        orderLeg=row.ODvr_Leg,
        driverRole=row.ODvr_Role,
    )


def convert_HTC300_G040_T013D_Dock_Order_Drivers(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    addOrderDriver(
        sqlConn,
        orderId=row.ODvr_OrderNo,
        driverUserId=row.ODvr_EmpID,
        orderLeg=row.ODvr_Leg,
        driverRole=row.ODvr_Role,
    )


def convert_HTC300_G040_T013E_Service_Order_Drivers(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    addOrderDriver(
        sqlConn,
        orderId=row.ODvr_OrderNo,
        driverUserId=row.ODvr_EmpID,
        orderLeg=row.ODvr_Leg,
        driverRole=row.ODvr_Role,
    )


def convert_HTC300_G040_T014A_Open_Order_Attachments(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    addOrderAttachment(
        sqlConn,
        orderId=row.Att_OrderNo,
        attachmentPath=row.Att_Path,
        fileSize=row.ATT_Size,
    )


def convert_HTC300_G040_T014B_Invoiced_Order_Attachments(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    addOrderAttachment(
        sqlConn,
        orderId=row.Att_OrderNo,
        attachmentPath=row.Att_Path,
        fileSize=row.ATT_Size,
    )


def convert_HTC300_G040_T014C_Remaining_Order_Attachments(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    addOrderAttachment(
        sqlConn,
        orderId=row.Att_OrderNo,
        attachmentPath=row.Att_Path,
        fileSize=row.ATT_Size,
    )


def convert_HTC300_G040_T014D_Dock_Order_Attachments(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    addOrderAttachment(
        sqlConn,
        orderId=row.Att_OrderNo,
        attachmentPath=row.Att_Path,
        fileSize=row.ATT_Size,
    )


def convert_HTC300_G040_T014E_Service_Order_Attachments(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    addOrderAttachment(
        sqlConn,
        orderId=row.Att_OrderNo,
        attachmentPath=row.Att_Path,
        fileSize=row.ATT_Size,
    )


def convert_HTC300_G040_T030_Orders_Update_History(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    if not row.Orders_OrderNbr:
        return
    addOrderChangeHistory(
        sqlConn,
        orderId=row.Orders_OrderNbr,
        userId=getUserIdFromUsername(sqlConn, row.Orders_UpdtLID),
        dateChanged=row.Orders_UpdtDate,
        changes=(
            safeLower(row.Orders_Changes.strip())
            if not row.Orders_Changes.strip() == ""
            else "N/A"
        ),
    )


def convert_HTC300_G050_T010_Accessorials(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    if safeLower(row.AccType) == "asrl":
        if safeLower(row.AccBasis) == "lb":
            basisType = "weight"
        elif safeLower(row.AccBasis) == "fxd":
            basisType = "fixed"
        elif safeLower(row.AccBasis) == "ask":
            basisType = "prompt"

        addAssessorial(
            sqlConn,
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
            notes=row.Acc_Comments,
        )
    """
    elif row.AccType.lower() == 'spcl':
        addSpecial(
            sqlConn,
            branchId=row.AccBrID,
            oldId=row.AccID,
            weekday=?,
            startTime=0,
            endTime=0,
            area='A',
            isActive=row.AccActive,
            amountCharged=?
        )
    """


def convert_HTC300_G050_T030_Accessorials_Update_History(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    assessorialType = "asdsa"

    if safeLower(assessorialType) == "asrl":
        addAssessorialChangeHistory(
            sqlConn,
            assessorialId=row.Acc_AccID,
            userId=getUserIdFromUsername(sqlConn, row.Acc_UpdtLID),
            dateChanged=row.Acc_UpdtDate,
            changes=(
                safeLower(row.Acc_Changes.strip())
                if not row.Acc_Changes.strip() == ""
                else "N/A"
            ),
        )
    elif safeLower(assessorialType) == "spcl":
        addSpecialChangeHistory(
            sqlConn,
            specialId=row.Acc_AccID,
            userId=getUserIdFromUsername(sqlConn, row.Acc_UpdtLID),
            dateChanged=row.Acc_UpdtDate,
            changes=(
                safeLower(row.Acc_Changes.strip())
                if not row.Acc_Changes.strip() == ""
                else "N/A"
            ),
        )


def convert_HTC300_G060_T010_Addresses(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    addressId = addAddress(
        sqlConn,
        addressLine1=row.FavAddrLn1,
        addressLine2=row.FavAddrLn2,
        cityName=row.FavCity,
        postalCode=row.FavZip,
        regionDetails={"isoCode": row.FavState},
        countryDetails={"isoCode3": row.FavCountry},
    )

    phoneId = addPhone(
        sqlConn,
        countryCode="1",
        areaCode=getPhoneAreaCode(row.FavPhone),
        phoneNumber=getPhoneNumber(row.FavPhone),
        phoneExtension=row.FavExt,
    )

    for assessorialId in getAssessorialIds(row.FavAssessorials):
        addLocationDefaultAssessorial(
            sqlConn, locationId=row.FavID, assessorialId=assessorialId
        )

    addLocation(
        sqlConn,
        locationId=row.FavID,
        branchId=row.FavBrID,
        companyName=row.FavCompany,
        locationName=row.FavLocnName,
        addressId=addressId,
        aciId=row.FavACIID if row.FavACIID != 0 else None,
        contactFirstName=row.FavFirstName,
        contactLastName=row.FavLastName,
        contactEmail=row.FavEMail,
        contactPhoneId=phoneId,
        isCarrier=row.FavCarrierYN,
        isLocal=row.FavLocalYN,
        isInternational=row.FavInternational,
        defaultWaitTime=row.FavWaitTimeDefault,
        isActive=row.FavActive,
    )


def convert_HTC300_G060_T030_Addresses_Update_History(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    addLocationChangeHistory(
        sqlConn,
        locationId=row.Addr_ID,
        userId=getUserIdFromUsername(sqlConn, row.Addr_UpdtLID),
        dateChanged=row.Addr_UpdtDate,
        changes=row.Addr_Chgs.strip() if not row.Addr_Chgs.strip() == "" else "N/A",
    )


def convert_HTC300_G070_T010_Rates(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
):
    pass


def convert_HTC300_G070_T030_Rates_Update_History(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
):
    pass


def convert_HTC300_G080_T010_Agents(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
):
    pass


def convert_HTC300_G080_T020_Agent_Certifications(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
):
    pass


def convert_HTC300_G080_T030_Agents_Change_History(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
):
    pass


def convert_HTC300_G090_T030_Staff_Chg_History(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
):
    pass


def convert_HTC300_G100_T020_Certification_Trainers(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
):
    pass


def convert_HTC300_G100_T021_Certifaction_Trainer_Change_History(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
):
    pass


def convert_HTC300_G100_T030_CertificationTestCatalogChgHistory(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
):
    pass


def convert_HTC400_G040_T010A_Orders(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    rateId = 1
    if row.M_Driver:
        driverName = row.M_Driver.strip()
    else:
        driverName = None

    addOrder(
        sqlConn,
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
        isWeightChargeCalculated=row.M_WgtChgsCalcYN,
    )


def convert_HTC400_G040_T011A_Assessorials(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    if row.OA_MinutesWaitTime:
        basisCount = row.OA_MinutesWaitTime
    elif row.OA_HowManyMiles:
        basisCount = row.OA_HowManyMiles
    elif row.OA_HowManyHrs:
        basisCount = row.OA_HowManyHrs
    else:
        basisCount = None

    addOrderAssessorial(
        sqlConn,
        orderId=row.OA_OrderNo,
        parentType=row.OA_AssParent,
        assessorialId=row.OA_AssID,
        basisCount=basisCount,
        totalCharge=row.OA_TotalCharges,
    )


def convert_HTC400_G040_T012A_Dims(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    addOrderDim(
        sqlConn,
        orderId=row.OD_OrderNo,
        unitType=row.OD_UnitType,
        unitQuantity=row.OD_UnitQty,
        dimHeight=row.OD_UnitHeight,
        dimLength=row.OD_UnitLength,
        dimWidth=row.OD_UnitWidth,
        unitWeight=row.OD_UnitWeight,
        dimWeight=row.OD_UnitDimWeight,
    )


def convert_HTC400_G040_T013A_Drivers(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    addOrderDriver(
        sqlConn,
        orderId=row.ODvr_OrderNo,
        driverUserId=row.ODvr_EmpID,
        orderLeg=row.ODvr_Leg,
        driverRole=row.ODvr_Role,
    )


def convert_HTC400_G040_T014A_Attachments(
    sqlConnFactory: Callable[[], SqlServerConn], row: PyODBCRow
) -> None:
    sqlConn = sqlConnFactory()
    addOrderAttachment(
        sqlConn,
        orderId=row.Att_OrderNo,
        attachmentPath=row.Att_Path,
        fileSize=row.Att_Size,
    )


def convert_HTC400_G900_T010_Archive_Event_Log(
    sqlConnFactory: Callable[[], SqlServerConn]
):
    sqlConn = sqlConnFactory()
    print("Completed [HTC400_G900_T010 Archive Event Log] Conversion.")
