from ...imports import *

def convert_HTC300_G030_T030_Customer_Update_History(conn : Connection):
    customer_change_historyInfo = conn.accessGetTableInfo('htc300', 'HTC300_G030_T030 Customer Update History')
    for row in customer_change_historyInfo:
        pass
    print('Completed [HTC300_G030_T030 Customer Update History] Conversion.')