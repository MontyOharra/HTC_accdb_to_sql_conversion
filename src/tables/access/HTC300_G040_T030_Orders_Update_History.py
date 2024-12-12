from ...imports import *

from ..sql.order_change_history import addOrderChangeHistory

def convert_HTC300_G040_T030_Orders_Update_History(conn : Connection, row):
    addOrderChangeHistory(
        conn,
        dateChanged=row.STAT_UpdtDate,
        orderStatusId=row.STAT_Seq,
        userId=getUserIdFromUsername(conn, row.STAT_UpdtLID), 
        changes=row.STAT_Changes if not row.STAT_Changes.strip() == '' else 'N/A'
    )