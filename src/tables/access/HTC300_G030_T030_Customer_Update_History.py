from ...imports import *

from ..sql.customer_change_history import addCustomerChangeHistory

def convert_HTC300_G030_T030_Customer_Update_History(conn : Connection, row):
    addCustomerChangeHistory(
        conn,
        dateChanged=row.STAT_UpdtDate,
        orderStatusId=row.STAT_Seq,
        userId=getUserIdFromUsername(conn, row.STAT_UpdtLID), 
        changes=row.STAT_Changes if not row.STAT_Changes.strip() == '' else 'N/A'
    )