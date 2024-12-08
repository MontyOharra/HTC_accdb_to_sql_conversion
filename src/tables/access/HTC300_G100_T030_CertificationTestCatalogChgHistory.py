from ...imports import *

def convert_HTC300_G100_T030_CertificationTestCatalogChgHistory(conn : Connection):
    certification_test_change_historyInfo = conn.accessGetTableInfo('htc300', 'HTC300_G100_T030 CertificationTestCatalogChgHistory')
    for row in certification_test_change_historyInfo:
        pass