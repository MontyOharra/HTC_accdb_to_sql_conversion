from ...imports import *

from ..sql.aci_data_change_history import addAciDataChangeHistory



def convert_HTC300_G010_T030_ACI_Update_History(conn : Connection):
    tableName = 'HTC300_G010_T030 ACI Update History'
    aci_data_change_historyInfo = conn.accessGetTableInfo('htc300', tableName)
    for i, row in enumerate(aci_data_change_historyInfo, start=1):
        sys.stdout.write(f"\rConverting [{tableName}] Table: Currently converting row ({i}/{len(aci_data_change_historyInfo)})\033[K")
        sys.stdout.flush()
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
    sys.stdout.write(f"\rCompleted [{tableName}] Conversion.\033[K\n")
    sys.stdout.flush()