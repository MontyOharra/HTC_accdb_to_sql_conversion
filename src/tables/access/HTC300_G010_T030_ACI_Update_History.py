from ...imports import *

from ..sql.aci_data_change_history import addAciDataChangeHistory



def convert_HTC300_G010_T030_ACI_Update_History(conn : Connection):
    aci_data_change_historyInfo = conn.accessGetTableInfo('htc300', 'HTC300_G010_T030 ACI Update History')
    for row in aci_data_change_historyInfo:
        userId = conn.sqlGetInfo('user', 'id', f"[username] = '{row.ACI_UpdtLID}'")
        if not userId:
            userId = 0
        else:
            userId = userId[0].id
        addAciDataChangeHistory(
            conn,
            aciDataId=row.ACI_LineNbr,
            userId=userId,
            dateChanged=row.ACI_UpdtDate,
            changes=row.ACI_Updates
        )
    print('Completed [HTC010_G000_T000 OrderType Values] Conversion.')