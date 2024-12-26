from ...imports import *

from ..sql.order_attachment import addOrderAttachment

def convert_HTC300_G040_T014E_Service_Order_Attachments(conn : Connection, row):
    addOrderAttachment(
      conn,
      orderId=row.Att_OrderNo,
      attachmentPath=row.Att_Path,
      fileSize=row.Att_Size
    )