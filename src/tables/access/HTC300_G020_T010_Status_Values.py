from ...imports import *

from ..sql.order_status import addOrderStatus

def convert_HTC300_G020_T010_Status_Values(conn : Connection):
    order_statusInfo = conn.accessGetTableInfo('htc300', 'HTC300_G020_T010 Status Values')
    for row in order_statusInfo:
        addOrderStatus(
          conn, 
          orderStatusName=row.Stat_Text,
          isOnManifest=row.OnManifest,
          isSetToAutoNotify=row.AutoNotify,
          isActive=row.Stat_Active
        )
    print('Completed [HTC300_G020_T010 Status Values] Conversion.')