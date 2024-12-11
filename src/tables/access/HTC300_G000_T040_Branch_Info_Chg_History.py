from ...imports import *

from ..sql.branch_change_history import addBranchChangeHistory

from ..sql.user import getUserIdFromUsername

def convert_HTC300_G000_T040_Branch_Info_Chg_History(conn : Connection):
    tableName = 'HTC300_G000_T040 Branch Info Chg History'
    branch_change_historyInfo = conn.accessGetTableInfo('htc300', tableName)
    for i, row in enumerate(branch_change_historyInfo, start=1):
        sys.stdout.write(f"\rConverting [{tableName}] Table: Currently converting row ({i}/{len(branch_change_historyInfo)})\033[K")
        sys.stdout.flush()
        userId = getUserIdFromUsername(conn, row.BrInfo_LID)
        addBranchChangeHistory(
            conn,
            branchId=row.BrInfo_BrID,
            userId=getUserIdFromUsername(userId),
            dateChanged=row.BrInfo_Now,
            changes=row.BrInfo_Chgs
        )
    sys.stdout.write(f"\rCompleted [{tableName}] Conversion.\033[K\n")
    sys.stdout.flush()