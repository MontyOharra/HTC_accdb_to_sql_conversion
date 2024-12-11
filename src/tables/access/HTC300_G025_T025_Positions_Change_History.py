from ...imports import *

def convert_HTC300_G025_T025_Positions_Change_History(conn : Connection):
    tableName = 'HTC300_G025_T025 Positions Change History'
    position_change_historyInfo = conn.accessGetTableInfo('htc300', tableName)
    for i, row in enumerate(position_change_historyInfo, start=1):
        sys.stdout.write(f"\rConverting [{tableName}] Table: Currently converting row ({i}/{len(position_change_historyInfo)})\033[K")
        sys.stdout.flush()
        position_change_historyInfo(
            conn,
            dateChanged=row.STAT_UpdtDate,
            orderStatusId=row.STAT_Seq,
            userId=getUserIdFromUsername(conn, row.STAT_UpdtLID), 
            changes=row.STAT_Changes if not row.STAT_Changes.strip() == '' else 'N/A'
        )
    sys.stdout.write(f"\rCompleted [{tableName}] Conversion.\033[K")
    sys.stdout.flush()