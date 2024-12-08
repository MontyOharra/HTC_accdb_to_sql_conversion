from ...imports import *

def convert_HTC300_G020_T030_Status_Update_History(conn : Connection):
    order_status_change_historyInfo = conn.accessGetTableInfo('htc300', 'HTC300_G020_T030 Status Update History')
    for row in order_status_change_historyInfo:
        pass