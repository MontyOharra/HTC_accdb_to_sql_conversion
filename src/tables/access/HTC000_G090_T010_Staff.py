from ...imports import *

from ..sql.user import addUser
from ..sql.address import addAddress
from ..sql.phone import addPhone

def convert_HTC000_G090_T010_Staff(conn : Connection):
    tableName = 'HTC000_G090_T010 Staff'
    userInfo = conn.accessGetTableInfo('htc000', tableName)
    for i, row in enumerate(userInfo, start=1):
        sys.stdout.write(f"\rConverting [{tableName}] Table: Currently converting row ({i}/{len(userInfo)})\033[K")
        sys.stdout.flush()
        phoneMainId = addPhone(
            conn,
            '1',
            getPhoneAreaCode(row.Staff_Phone),
            getPhoneNumber(row.Staff_Phone),
            ''
        )
        phoneMobileId = addPhone(
            conn,
            '1',
            getPhoneAreaCode(row.Staff_Mobile),
            getPhoneNumber(row.Staff_Mobile),
            ''
        )
        phoneHomeId = addPhone(
            conn,
            '1',
            getPhoneAreaCode(row.Staff_Home_Phone),
            getPhoneNumber(row.Staff_Home_Phone),
            ''
        )
        addressId = addAddress(
            conn,
            row.Staff_Home_Street1,
            row.Staff_Home_Street2,
            row.Staff_Home_City,
            correctPostalCode(row.Staff_Home_Zip),
            {'isoCode' : row.Staff_Home_StAbbr},
            {'isoCode3' : row.Staff_Home_Country}
        )
        
        addUser(
            conn,
            branchId=row.Staff_BrID,
            username=row.Staff_Login,
            namePrefix=row.Staff_NamePrefix if row.Staff_NamePrefix else None,
            firstName=row.Staff_FirstName,
            lastName=row.Staff_LastName,
            nameSuffix=row.Staff_NameSuffix if row.Staff_NamePrefix else None,
            email=row.Staff_Email,
            phoneMainId=phoneMainId,
            phoneMobileId=phoneMobileId,
            tsaType=row.Staff_TSA_Type if row.Staff_NamePrefix else None,
            tsaNumber=row.Staff_TSA_Number if row.Staff_NamePrefix else None,
            tsaTaken=row.Staff_TSA_Taken,
            positionId=row.Staff_RoleID,
            commissionRate=row.Staff_CommRate,
            addressId=addressId,
            phoneHomeId=phoneHomeId,
            dateHired=row.Staff_DateOfHire,
            dateTerminated=row.Staff_DateOfTermination,
            passwordHash=row.Staff_Password if row.Staff_Password else '',
            passwordSalt='',
            isSecurityCoordinator=row.Staff_SecCoord,
            isTsaTrainer=row.Staff_TSATrainer,
            isDefaultDocOwner=row.Staff_DefaultDocOwner,
            isActive=row.Staff_Active
        )
    sys.stdout.write(f"\rCompleted [{tableName}] Conversion.\033[K\n")
    sys.stdout.flush()