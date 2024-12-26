from ...imports import *

def convert_HTC300_G080_T010_Agents(conn : Connection):
    agentInfo = conn.accessGetTableInfo('htc300', 'HTC300_G080_T010 Agents')
    for row in agentInfo:
        pass
    print('Completed [HTC300_G080_T010 Agents] Conversion.')