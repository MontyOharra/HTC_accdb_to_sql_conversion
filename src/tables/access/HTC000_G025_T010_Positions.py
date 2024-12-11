from ...imports import *

from ..sql.position import addPosition

def convert_HTC000_G025_T010_Positions(conn : Connection):
    tableName = 'HTC000_G025_T010 Positions'
    positionInfo = conn.accessGetTableInfo('htc000', tableName)
    for i, row in enumerate(positionInfo, start=1):
        sys.stdout.write(f"\rConverting [{tableName}] Table: Currently converting row ({i}/{len(positionInfo)})\033[K")
        sys.stdout.flush()
        addPosition(
            conn,
            positionName=row.Posn_Title,
            securityLevel=row.Posn_SecurityLevel,
            isActive=row.Posn_Status,
            branchId=row.Posn_BrID
        )
    sys.stdout.write(f"\rCompleted [{tableName}] Conversion.\033[K\n")
    sys.stdout.flush()