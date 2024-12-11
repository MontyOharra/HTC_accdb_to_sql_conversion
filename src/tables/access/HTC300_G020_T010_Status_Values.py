from ...imports import *

from ..sql.order_status import addOrderStatus

def convert_HTC300_G020_T010_Status_Values(conn : Connection):
    tableName = 'HTC300_G020_T010 Status Values'
    order_statusInfo = conn.accessGetTableInfo('htc300', 'HTC300_G020_T010 Status Values')
    for i, row in enumerate(order_statusInfo, start=1):
        sys.stdout.write(f"\rConverting [{tableName}] Table: Currently converting row ({i}/{len(order_statusInfo)})\033[K")
        sys.stdout.flush()
        addOrderStatus(
          conn, 
          orderStatusName=row.Stat_Text,
          branchId=row.Stat_BrID,
          isOnManifest=row.OnManifest,
          isSetToAutoNotify=row.AutoNotify,
          isActive=row.Stat_Active
        )
    sys.stdout.write(f"\rCompleted [{tableName}] Conversion.\033[K\n")
    sys.stdout.flush()