from ...imports import *

from ..sql.certification_test import addCertificationTest

def convert_HTC010_G100_T010_CertificationTestCatalog(conn : Connection):
    tableName = 'HTC010_G100_T010 CertificationTestCatalog'
    certification_testInfo = conn.accessGetTableInfo('htc010', tableName)
    for i, row in enumerate(certification_testInfo, start=1):
        sys.stdout.write(f"\rConverting [{tableName}] Table: Currently converting row ({i}/{len(certification_testInfo)})\033[K")
        sys.stdout.flush()
        addCertificationTest(
            conn,
            certificationName=row.TestTitle,
            certificationTestTrainerId=row.TestTrainerID,
            isActive=row.TestStatus
        )
    sys.stdout.write(f"\rCompleted [{tableName}] Conversion.\033[K\n")
    sys.stdout.flush()