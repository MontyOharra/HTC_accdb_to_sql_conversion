from ...imports import *

def convert_HTC300_G025_T025_Positions_Change_History(conn : Connection):
    position_change_historyInfo = conn.accessGetTableInfo('htc300', 'HTC300_G025_T025 Positions Change History')
    for row in position_change_historyInfo:
        pass