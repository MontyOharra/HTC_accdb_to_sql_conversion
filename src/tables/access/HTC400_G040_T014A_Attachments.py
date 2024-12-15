from ...imports import *

from ..sql.order_attachment import addOrderAttachment

def convert_HTC400_G040_T014A_Attachments(conn : Connection, row):
    addOrderAttachment(
      conn,
      orderId=row.Att_OrderNo,
      attachmentPath=row.Att_Path,
      fileSize=row.Att_Size
    )