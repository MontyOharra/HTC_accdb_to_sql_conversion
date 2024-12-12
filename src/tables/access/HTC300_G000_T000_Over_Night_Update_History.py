from ...imports import *

from ..sql.overnight_maintenance_history import addOvernightMaintenanceHistory

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