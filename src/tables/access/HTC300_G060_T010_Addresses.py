from ...imports import *

def convert_HTC300_G060_T010_Addresses(conn : Connection):
    locationInfo = conn.accessGetTableInfo('htc300', 'HTC300_G060_T010 Addresses')
    for row in locationInfo:
        pass