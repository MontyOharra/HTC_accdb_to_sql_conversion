from ...imports import *

from ..sql.order_assessorial import addOrderAssessorial

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