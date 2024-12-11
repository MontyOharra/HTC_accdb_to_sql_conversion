from ...imports import *

from ..sql.order_status_change_history import addOrderStatusChangeHistory

def convert_HTC300_G020_T030_Status_Update_History(conn : Connection):
    order_status_change_historyInfo = conn.accessGetTableInfo('htc300', 'HTC300_G020_T030 Status Update History')
    for row in order_status_change_historyInfo:
        addOrderStatusChangeHistory(
            conn,
            dateChanged=row.STAT_UpdtDate,
            orderStatusId=row.STAT_Seq,
            userId=getUserIdFromUsername(row.Stat_UpdtLID), 
            changes=row.STAT_Changes
        )
    print('Completed [HTC300_G020_T030 Status Update History] Conversion.')