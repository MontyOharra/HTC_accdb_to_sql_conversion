from ...imports import *

from ..sql.customer_change_history import addCustomerChangeHistory

def convert_HTC300_G030_T030_Customer_Update_History(conn : Connection, row):
    if row.Cust_CoID == 1 and row.Cust_BrID == 1:
      addCustomerChangeHistory(
          conn,
          dateChanged=combineDateTime(row.Cust_UpdtDate, row.Cust_UpdtTime),
          customerId=row.Cust_CustomerID,
          userId=getUserIdFromUsername(conn, row.Cust_UpdtLID), 
          changes=row.Cust_FldUpdts.strip() if not row.Cust_FldUpdts.strip() == '' else 'N/A'
      )