from ...imports import *

from ..sql.order_change_history import addOrderChangeHistory

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