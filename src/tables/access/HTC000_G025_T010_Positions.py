from ...imports import *

from ..sql.position import addPosition

def convert_HTC000_G025_T010_Positions(conn : Connection):
    positionInfo = conn.accessGetTableInfo('htc000', 'HTC000_G025_T010 Positions')
    for row in positionInfo:
        addPosition(
            conn,
            positionName=row.Posn_Title,
            securityLevel=row.Posn_SecurityLevel,
            isActive=row.Posn_Status,
            branchId=row.Posn_BrID
        )
    print('Completed [HTC000_G025_T010 Positions] Conversion.')