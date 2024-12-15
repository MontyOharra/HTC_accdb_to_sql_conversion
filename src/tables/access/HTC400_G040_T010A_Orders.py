from ...imports import *

from ..sql.order import addOrder

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