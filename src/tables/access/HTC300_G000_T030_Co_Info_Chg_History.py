from ...imports import *

from ..sql.company_change_history import addCompanyChangeHistory

def convert_HTC300_G000_T030_Co_Info_Chg_History(conn : Connection):
    company_change_historyInfo = conn.accessGetTableInfo('htc300', 'HTC300_G000_T030 Co Info Chg History')
    for row in company_change_historyInfo:
        userId = getUserIdFromUsername(conn, row.CoInfo_LID)
        addCompanyChangeHistory(
            conn,
            companyId=row.CoInfo_CoID,
            userId=userId,
            dateChanged=row.CoInfo_Now,
            changes=row.CoInfo_Chgs
        )
    print('Completed [HTC010_G000_T000 OrderType Values] Conversion.')