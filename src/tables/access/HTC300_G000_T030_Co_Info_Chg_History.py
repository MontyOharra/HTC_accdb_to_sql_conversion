from ...imports import *

from ..sql.company_change_history import addCompanyChangeHistory

def convert_HTC300_G000_T030_Co_Info_Chg_History(conn : Connection, row):
    userId = getUserIdFromUsername(conn, row.CoInfo_LID)
    addCompanyChangeHistory(
        conn,
        companyId=row.CoInfo_CoID,
        userId=userId,
        dateChanged=row.CoInfo_Now,
        changes=row.CoInfo_Chgs
    )