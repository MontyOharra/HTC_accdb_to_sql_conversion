from ...imports import *

from ..sql.branch_change_history import addBranchChangeHistory

from ..sql.user import getUserIdFromUsername

def convert_HTC300_G000_T040_Branch_Info_Chg_History(conn : Connection):
    branch_change_historyInfo = conn.accessGetTableInfo('htc300', 'HTC300_G000_T040 Branch Info Chg History')
    for row in branch_change_historyInfo:
        userId = getUserIdFromUsername(conn, row.BrInfo_LID)
        addBranchChangeHistory(
            conn,
            branchId=row.BrInfo_BrID,
            userId=getUserIdFromUsername(userId),
            dateChanged=row.BrInfo_Now,
            changes=row.BrInfo_Chgs
        )
    print('Completed [HTC010_G000_T000 OrderType Values] Conversion.')