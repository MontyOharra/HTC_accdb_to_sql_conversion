from ...imports import *

def convert_HTC300_G100_T020_Certification_Trainers(conn : Connection):
    certification_test_trainerInfo = conn.accessGetTableInfo('htc300', 'HTC300_G100_T020 Certification Trainers')
    for row in certification_test_trainerInfo:
        pass
    print('Completed [HTC300_G100_T020 Certification Trainers] Conversion.')