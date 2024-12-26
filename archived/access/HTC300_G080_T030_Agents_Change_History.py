from ...imports import *

def convert_HTC300_G080_T030_Agents_Change_History(conn : Connection):
    agent_change_historyInfo = conn.accessGetTableInfo('htc300', 'HTC300_G080_T030 Agents Change History')
    for row in agent_change_historyInfo:
        pass
    print('Completed [HTC300_G080_T030 Agents Change History] Conversion.')