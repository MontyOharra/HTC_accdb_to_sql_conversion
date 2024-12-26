from ...imports import *

from ..sql.order_type import addOrderType

def convert_HTC010_G000_T000_OrderType_Values(conn : Connection, row):
    addOrderType(
        conn,
        orderTypeId=row.OrdType_ID,
        orderTypeName=row.OrdType_Title
    )