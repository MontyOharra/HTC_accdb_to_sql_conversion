from ...imports import *

from ..sql.order_dim import addOrderDim

def convert_HTC300_G040_T012B_Invoiced_Order_Dims(conn : Connection, row):
    addOrderDim(
        conn,
        orderId = row.OD_OrderNo,
        unitType=row.OD_UnitType,
        unitQuantity=row.OD_UnitQty,
        dimHeight=row.OD_UnitHeight,
        dimLength=row.OD_UnitLength,
        dimWidth=row.OD_UnitWidth,
        unitWeight=row.OD_UnitWeight,
        dimWeight=row.OD_UnitDimWeight,
    )