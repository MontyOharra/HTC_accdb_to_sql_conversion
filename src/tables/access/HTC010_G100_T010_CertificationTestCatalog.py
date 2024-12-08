from ...imports import *

from ..sql.certification_test import addCertificationTest

def convert_HTC010_G100_T010_CertificationTestCatalog(conn : Connection):
    certification_testInfo = conn.accessGetTableInfo('htc010', 'HTC010_G100_T010 CertificationTestCatalog')
    for row in certification_testInfo:
        addCertificationTest(
            conn,
            certificationName=row.TestTitle,
            certificationTestTrainerId=row.TestTrainerID,
            isActive=row.TestStatus
        )
    print('Completed [HTC010_G100_T010 CertificationTestCatalog] Conversion.')