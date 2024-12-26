from ...imports import *

agentFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="customer_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="email_address", fieldDetails="NVARCHAR(127) NOT NULL"),
    Field(fieldName="first_name", fieldDetails="NVARCHAR(50)"),
    Field(fieldName="last_name", fieldDetails="NVARCHAR(50)"),
    Field(fieldName="phone_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="mobile_phone_id", fieldDetails="INTEGER"),
    Field(fieldName="fax_id", fieldDetails="INTEGER"),
    Field(fieldName="is_set_to_auto_notify_email", fieldDetails="BIT NOT NULL DEFAULT (0)"),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL DEFAULT (1)"),
]

agentIndexes: List[Index] = [
]

agentForeignKeys: List[ForeignKey] = [
    ForeignKey('agent', 'customer_id', 'customer', 'id'),
    ForeignKey('agent', 'phone_id', 'phone', 'id'),
    ForeignKey('agent', 'mobile_phone_id', 'phone', 'id'),
    ForeignKey('agent', 'fax_id', 'fax', 'id'),
]

def createAgentTable(conn):
    agentTable = SqlTable('agent', conn, agentFields, agentIndexes, agentForeignKeys)
    agentTable.createTable()
    agentTable.addIndexes()

    return agentTable

def addAgent(
    conn : Connection,
    customerId : int,
    emailAddress : str,
    firstName : str,
    lastName : str,
    phoneId : int,
    mobilePhoneId : int,
    faxId : int,
    isSetToAutoNotifyEmail : bool,
    isActive : bool,
) -> int:
    agentRow = conn.sqlGetInfo(
        'agent',
        'id',
        whereDetails={
            'customer_id': customerId,
            'email_address': emailAddress,
            'first_name': firstName,
            'last_name': lastName,
            'phone_id': phoneId,
            'mobile_phone_id': mobilePhoneId,
            'fax_id': faxId,
            'is_set_to_auto_notify_email': isSetToAutoNotifyEmail,
            'is_active': isActive
        }
    )
    if agentRow:
        return agentRow[0].id

    data = {
        'customer_id' : customerId,
        'email_address' : emailAddress,
        'first_name' : firstName,
        'last_name' : lastName,
        'phone_id' : phoneId,
        'mobile_phone_id' : mobilePhoneId,
        'fax_id' : faxId,
        'is_set_to_auto_notify_email' : isSetToAutoNotifyEmail,
        'is_active' : isActive,
    }
    conn.sqlInsertRow('agent', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('agent')