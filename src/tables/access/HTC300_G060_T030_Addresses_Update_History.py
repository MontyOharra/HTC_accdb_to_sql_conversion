from ...imports import *

def convert_HTC300_G060_T030_Addresses_Update_History(conn : Connection):
    location_change_historyInfo = conn.accessGetTableInfo('htc300', 'HTC300_G060_T030 Addresses Update History')
    for row in location_change_historyInfo:
        pass