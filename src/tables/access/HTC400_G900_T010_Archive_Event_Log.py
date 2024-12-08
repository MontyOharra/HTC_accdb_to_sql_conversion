from ...imports import *

def convert_HTC400_G900_T010_Archive_Event_Log(conn : Connection):
    archive_error_logInfo = conn.accessGetTableInfo('htc400', 'HTC400_G900_T010 Archive Event Log')
    for row in archive_error_logInfo:
        pass