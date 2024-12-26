from ...imports import *

from ..sql.order_driver import addOrderDriver

def convert_HTC400_G040_T013A_Drivers(conn : Connection, row):
    addOrderDriver(
      conn,
      orderId=row.ODvr_OrderNo,
      driverUserId=row.ODvr_EmpID,
      orderLeg=row.ODvr_Leg,
      driverRole=row.ODvr_Role
    )