from ...imports import *

def convert_HTC300_G030_T010_Customers(conn : Connection):
    customerInfo = conn.accessGetTableInfo('htc300', 'HTC300_G030_T010 Customers')
    for row in customerInfo:
        pass
    print('Completed [HTC300_G030_T010 Customers] Conversion.')