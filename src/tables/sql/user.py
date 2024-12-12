from ...imports import *

userFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="username", fieldDetails="NVARCHAR(63) UNIQUE NOT NULL"),
    Field(fieldName="email", fieldDetails="NVARCHAR(255) NOT NULL"),
    Field(fieldName="password_hash", fieldDetails="NVARCHAR(255)"),
    Field(fieldName="password_salt", fieldDetails="NVARCHAR(32)"),
    Field(fieldName="name_prefix", fieldDetails="NVARCHAR(6)"),
    Field(fieldName="first_name", fieldDetails="NVARCHAR(31)"),
    Field(fieldName="last_name", fieldDetails="NVARCHAR(31)"),
    Field(fieldName="name_suffix", fieldDetails="NVARCHAR(6)"),
    Field(fieldName="address_id", fieldDetails="INTEGER"),
    Field(fieldName="branch_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="commission_rate", fieldDetails="MONEY NOT NULL"),
    Field(fieldName="date_hired", fieldDetails="DATETIME2"),
    Field(fieldName="date_terminated", fieldDetails="DATETIME2"),
    Field(fieldName="phone_main_id", fieldDetails="INTEGER"),
    Field(fieldName="phone_home_id", fieldDetails="INTEGER"),
    Field(fieldName="phone_mobile_id", fieldDetails="INTEGER"),
    Field(fieldName="position_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="tsa_number", fieldDetails="NVARCHAR(12)"),
    Field(fieldName="tsa_type", fieldDetails="NVARCHAR(10)"),
    Field(fieldName="tsa_taken", fieldDetails="NVARCHAR(31)"),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL"),
    Field(fieldName="is_default_doc_owner", fieldDetails="BIT NOT NULL"),
    Field(fieldName="is_security_coordinator", fieldDetails="BIT NOT NULL"),
    Field(fieldName="is_tsa_trainer", fieldDetails="BIT NOT NULL"),
]

userIndexes: List[Index] = [
]

userForeignKeys: List[ForeignKey] = [
    ForeignKey('user', 'address_id', 'address', 'id'),
    ForeignKey('user', 'branch_id', 'branch', 'id'),
    ForeignKey('user', 'phone_main_id', 'phone', 'id'),
    ForeignKey('user', 'phone_home_id', 'phone', 'id'),
    ForeignKey('user', 'phone_mobile_id', 'phone', 'id'),
    ForeignKey('user', 'position_id', 'position', 'id'),
]

def createUserTable(conn):
    userTable = SqlTable('user', conn, userFields, userIndexes, userForeignKeys)
    userTable.createTable()
    userTable.addIndexes()

    return userTable

def addUser(
    conn : Connection,
    userId : int,
    username : str,
    email : str,
    passwordHash : str,
    passwordSalt : str,
    namePrefix : str,
    firstName : str,
    lastName : str,
    nameSuffix : str,
    addressId : int,
    branchId : int,
    commissionRate : float,
    dateHired : str,
    dateTerminated : str,
    phoneMainId : int,
    phoneHomeId : int,
    phoneMobileId : int,
    positionId : int,
    tsaNumber : str,
    tsaType : str,
    tsaTaken : str,
    isActive : bool,
    isDefaultDocOwner : bool,
    isSecurityCoordinator : bool,
    isTsaTrainer : bool,
) -> int:
    userRow = conn.sqlGetInfo(
        'user',
        'id',
        whereDetails    ={
            'username': username,
            'email': email,
            'password_hash': passwordHash,
            'password_salt': passwordSalt,
            'name_prefix': namePrefix,
            'first_name': firstName,
            'last_name': lastName,
            'name_suffix': nameSuffix,
            'address_id': addressId,
            'branch_id': branchId,
            'commission_rate': commissionRate,
            'date_hired': dateHired,
            'date_terminated': dateTerminated,
            'phone_main_id': phoneMainId,
            'phone_home_id': phoneHomeId,
            'phone_mobile_id': phoneMobileId,
            'position_id': positionId,
            'tsa_number': tsaNumber,
            'tsa_type': tsaType,
            'tsa_taken': tsaTaken,
            'is_active': isActive,
            'is_default_doc_owner': isDefaultDocOwner,
            'is_security_coordinator': isSecurityCoordinator,
            'is_tsa_trainer': isTsaTrainer
        }
    )
    if userRow:
        return userRow[0].id
    data = {
        'username' : username,
        'email' : email,
        'password_hash' : passwordHash,
        'password_salt' : passwordSalt,
        'name_prefix' : namePrefix,
        'first_name' : firstName,
        'last_name' : lastName,
        'name_suffix' : nameSuffix,
        'address_id' : addressId,
        'branch_id' : branchId,
        'commission_rate' : commissionRate,
        'date_hired' : dateHired,
        'date_terminated' : dateTerminated,
        'phone_main_id' : phoneMainId,
        'phone_home_id' : phoneHomeId,
        'phone_mobile_id' : phoneMobileId,
        'position_id' : positionId,
        'tsa_number' : tsaNumber,
        'tsa_type' : tsaType,
        'tsa_taken' : tsaTaken,
        'is_active' : isActive,
        'is_default_doc_owner' : isDefaultDocOwner,
        'is_security_coordinator' : isSecurityCoordinator,
        'is_tsa_trainer' : isTsaTrainer,
    }
    conn.sqlInsertRow('user', data, insertId=userId)
    conn.commit()

    return conn.sqlGetLastIdCreated('user')


def getUserIdFromUsername(conn : Connection, username : str | None) -> int:
    if username == None:
        return None
    if username.strip() == "":
        return None
    
    userRow = conn.sqlGetInfo('user', 'id', f"[username] = '{username}'")
    if not userRow:
        return None
    
    return userRow[0].id