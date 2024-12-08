from ...imports import *

from ..sql.order_type import addOrderType

def convert_HTC010_G000_T000_OrderType_Values(conn : Connection):
    order_typeInfo = conn.accessGetTableInfo('htc010', 'HTC010_G000_T000 OrderType Values')
    for row in order_typeInfo:
        addOrderType(
            conn,
            orderTypeName=row.OrdType_Title
        )
        
    print('Completed [HTC010_G000_T000 OrderType Values] Conversion.')