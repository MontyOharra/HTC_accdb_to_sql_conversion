from ....imports import *

from ..sql.certification_test import addCertificationTest
    
def convert_HTC010_G100_T010_CertificationTestCatalog(conn : Connection, row):
    addCertificationTest(
      conn,
      certificationTestId=row.TestID,
      certificationName=row.TestTitle,
      certificationTestTrainerId=row.TestTrainerID,
      isActive=row.TestStatus
    )