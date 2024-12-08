from ...imports import *

def convert_HTC300_G090_T030_Staff_Chg_History(conn : Connection):
    user_change_historyInfo = conn.accessGetTableInfo('htc300', 'HTC300_G090_T030 Staff Chg History')
    for row in user_change_historyInfo:
        pass