from ...imports import *

from ..sql.order_driver import addOrderDriver

def convert_HTC300_G040_T013E_Service_Order_Drivers(conn : Connection, row):
    addOrderDriver(
      conn,
      orderId=row.ODvr_OrderNo,
      driverUserId=row.ODvr_EmpID,
      orderLeg=row.ODvr_Leg,
      driverRole=row.ODvr_Role
    )