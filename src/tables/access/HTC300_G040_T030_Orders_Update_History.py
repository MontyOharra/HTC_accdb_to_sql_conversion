from ...imports import *

def convert_HTC300_G040_T030_Orders_Update_History(conn : Connection):
    order_change_historyInfo = conn.accessGetTableInfo('htc300', 'HTC300_G040_T030 Orders Update History')
    for row in order_change_historyInfo:
        pass
    print('Completed [HTC300_G040_T030 Orders Update History] Conversion.')