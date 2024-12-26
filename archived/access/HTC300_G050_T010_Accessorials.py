from ...imports import *

from ..sql.assessorial import addAssessorial
from ..sql.special import addSpecial

def convert_HTC300_G050_T010_Accessorials(conn : Connection, row):
    if row.AccType.lower() == 'asrl':
        if row.AccBasis.lower() == 'lb':
            basisType = 'weight'
        elif row.AccBasis.lower() == 'fxd':
            basisType = 'fixed'
        elif row.AccBasis.lower() == 'ask':
            basisType = 'prompt'
            
        addAssessorial(
            conn,
            branchId=row.AccBrID,
            assessorialId=row.AccID,
            assessorialName=row.AccDesc,
            isActive=row.AccActive,
            minCharge=row.AccMinCharge,
            basisType=basisType,
            userPrompt=row.Acc_Question,
            basisPortion=row.AccPortion,
            basisRate=row.AccRate,
            dateCreated=row.Acc_DateAdded,
            notes=row.Acc_Comments
        )
'''    elif row.AccType.lower() == 'spcl':
        addSpecial(
            conn,
            branchId=row.AccBrID,
            oldId=row.AccID,
            weekday=,
            startTime=0,
            endTime=0,
            area='A',
            isActive=row.AccActive,
            amountCharged
        )'''