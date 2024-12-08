from ...imports import *

def convert_HTC300_G070_T030_Rates_Update_History(conn : Connection):
    rate_change_historyInfo = conn.accessGetTableInfo('htc300', 'HTC300_G070_T030 Rates Update History')
    for row in rate_change_historyInfo:
        pass