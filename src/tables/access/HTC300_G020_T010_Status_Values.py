from ...imports import *

def convert_HTC300_G020_T010_Status_Values(conn : Connection):
    order_statusInfo = conn.accessGetTableInfo('htc300', 'HTC300_G020_T010 Status Values')
    for row in order_statusInfo:
        pass