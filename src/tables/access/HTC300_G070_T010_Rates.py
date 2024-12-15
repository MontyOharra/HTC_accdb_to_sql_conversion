from ...imports import *

def convert_HTC300_G070_T010_Rates(conn : Connection):
    rate_areaInfo = conn.accessGetTableInfo('htc300', 'HTC300_G070_T010 Rates')
    for row in rate_areaInfo:
        pass
    print('Completed [HTC300_G070_T010 Rates] Conversion.')
