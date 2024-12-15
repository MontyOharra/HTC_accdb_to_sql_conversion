from ...imports import *

from ..sql.order_status import addOrderStatus

def convert_HTC300_G020_T010_Status_Values(conn : Connection, row):
    addOrderStatus(
      conn, 
      orderStatusId=row.Stat_Seq,
      sequenceNumber=row.Stat_Seq,
      orderStatusName=row.Stat_Text,
      branchId=row.Stat_BrID,
      isOnManifest=row.OnManifest,
      isSetToAutoNotify=row.AutoNotify,
      isActive=row.Stat_Active
    )