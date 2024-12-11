from ...imports import *

from ..sql.order_type import addOrderType

def convert_HTC010_G000_T000_OrderType_Values(conn : Connection):
    tableName = 'HTC010_G000_T000 OrderType Values'
    order_typeInfo = conn.accessGetTableInfo('htc010', tableName)
    for i, row in enumerate(order_typeInfo, start=1):
        sys.stdout.write(f"\rConverting [{tableName}] Table: Currently converting row ({i}/{len(tableName)})\033[K")
        sys.stdout.flush()
        addOrderType(
            conn,
            orderTypeName=row.OrdType_Title
        )
        
    sys.stdout.write(f"\rCompleted [{tableName}] Conversion.\033[K\n")
    sys.stdout.flush()