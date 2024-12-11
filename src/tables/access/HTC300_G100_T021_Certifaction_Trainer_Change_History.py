from ...imports import *

def convert_HTC300_G100_T021_Certifaction_Trainer_Change_History(conn : Connection):
    certification_trainer_change_historyInfo = conn.accessGetTableInfo('htc300', 'HTC300_G100_T021 Certifaction Trainer Change History')
    for row in certification_trainer_change_historyInfo:
        pass
    print('Completed [HTC300_G100_T021 Certifaction Trainer Change History] Conversion.')