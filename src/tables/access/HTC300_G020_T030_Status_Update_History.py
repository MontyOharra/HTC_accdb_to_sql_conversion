from ...imports import *

from ..sql.order_status_change_history import addOrderStatusChangeHistory

def convert_HTC300_G020_T030_Status_Update_History(conn : Connection):
    tableName = 'HTC300_G020_T030 Status Update History'
    order_status_change_historyInfo = conn.accessGetTableInfo('htc300', tableName)
    for i, row in enumerate(order_status_change_historyInfo, start=1):
        sys.stdout.write(f"\rConverting [{tableName}] Table: Currently converting row ({i}/{len(order_status_change_historyInfo)})\033[K")
        sys.stdout.flush()
        addOrderStatusChangeHistory(
            conn,
            dateChanged=row.STAT_UpdtDate,
            orderStatusId=row.STAT_Seq,
            userId=getUserIdFromUsername(conn, row.STAT_UpdtLID), 
            changes=row.STAT_Changes if not row.STAT_Changes.strip() == '' else 'N/A'
        )
    sys.stdout.write(f"\rCompleted [{tableName}] Conversion.\033[K")
    sys.stdout.flush()