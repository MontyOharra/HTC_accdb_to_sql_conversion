from ...imports import *

from ..sql.position import addPosition

def convert_HTC000_G025_T010_Positions(conn : Connection, row):
    addPosition(
        conn,
        positionId=row.Posn_ID,
        positionName=row.Posn_Title,
        securityLevel=row.Posn_SecurityLevel,
        isActive=row.Posn_Status,
        branchId=row.Posn_BrID
    )