from ...imports import *

from ..sql.assessorial_change_history import addAssessorialChangeHistory
from ..sql.special_change_history import addSpecialChangeHistory

def convert_HTC300_G050_T030_Accessorials_Update_History(conn : Connection, row):
    assessorialType = conn.accessGetTableInfo('htc300', 'HTC300_G050_T010 Accessorials', 'AccType', whereDetails={'AccID': row.Acc_AccID})[0].AccType
    
    if assessorialType.lower() == 'asrl':
        addAssessorialChangeHistory(
            conn,
            assessorialId=row.Acc_AccID,
            userId=getUserIdFromUsername(conn, row.Acc_UpdtLID),
            dateChanged=row.Acc_UpdtDate,
            changes=row.Acc_Changes.strip() if not row.Acc_Changes.strip() == '' else 'N/A'
        )
    elif assessorialType.lower() == 'spcl':
        addSpecialChangeHistory(
            conn,
            specialId=row.Acc_AccID,
            userId=getUserIdFromUsername(conn, row.Acc_UpdtLID),
            dateChanged=row.Acc_UpdtDate,
            changes=row.Acc_Changes.strip() if not row.Acc_Changes.strip() == '' else 'N/A'
        )