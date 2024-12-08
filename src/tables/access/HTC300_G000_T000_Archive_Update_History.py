from ...imports import *

from ..sql.archive_history import addArchiveHistory

def convert_HTC300_G000_T000_Archive_Update_History(conn : Connection):
    archive_historyInfo = conn.accessGetTableInfo('htc300', 'HTC300_G000_T000 Archive Update History')
    for row in archive_historyInfo:
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
    print('Completed [HTC300_G000_T000 Archive Update History] Conversion.')