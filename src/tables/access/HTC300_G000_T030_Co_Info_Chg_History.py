from ...imports import *

from ..sql.company_change_history import addCompanyChangeHistory

def convert_HTC300_G000_T030_Co_Info_Chg_History(conn : Connection):
    tableName = 'HTC300_G000_T030 Co Info Chg History'
    company_change_historyInfo = conn.accessGetTableInfo('htc300', tableName)
    for i, row in enumerate(company_change_historyInfo, start=1):
        sys.stdout.write(f"\rConverting [{tableName}] Table: Currently converting row ({i}/{len(company_change_historyInfo)})\033[K")
        sys.stdout.flush()
        userId = getUserIdFromUsername(conn, row.CoInfo_LID)
        addCompanyChangeHistory(
            conn,
            companyId=row.CoInfo_CoID,
            userId=userId,
            dateChanged=row.CoInfo_Now,
            changes=row.CoInfo_Chgs
        )
    sys.stdout.write(f"\rCompleted [{tableName}] Conversion.\033[K\n")
    sys.stdout.flush()