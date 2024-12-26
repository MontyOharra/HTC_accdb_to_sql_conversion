from ...imports import *

from ..sql.order_status_change_history import addOrderStatusChangeHistory

def convert_HTC300_G020_T030_Status_Update_History(conn : Connection, row):
    addOrderStatusChangeHistory(
        conn,
        dateChanged=row.STAT_UpdtDate,
        orderStatusId=row.STAT_Seq,
        userId=getUserIdFromUsername(conn, row.STAT_UpdtLID), 
        changes=row.STAT_Changes if not row.STAT_Changes.strip() == '' else 'N/A'
    )