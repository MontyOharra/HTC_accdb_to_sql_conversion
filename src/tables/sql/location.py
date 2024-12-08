from ...imports import *

locationFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="branch_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="company_name", fieldDetails="NVARCHAR(127)"),
    Field(fieldName="location_name", fieldDetails="NVARCHAR(127)"),
    Field(fieldName="address_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="aci_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="contact_first_name", fieldDetails="NVARCHAR(31)"),
    Field(fieldName="contact_last_name", fieldDetails="NVARCHAR(31)"),
    Field(fieldName="contact_email", fieldDetails="NVARCHAR(127)"),
    Field(fieldName="contact_phone_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="is_carrier", fieldDetails="BIT NOT NULL DEFAULT (0)"),
    Field(fieldName="is_local", fieldDetails="BIT NOT NULL DEFAULT (0)"),
    Field(fieldName="is_international", fieldDetails="BIT NOT NULL DEFAULT (0)"),
    Field(fieldName="default_wait_time", fieldDetails="INTEGER"),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL DEFAULT (1)"),
]

locationIndexes: List[Index] = [
]

locationForeignKeys: List[ForeignKey] = [
    ForeignKey('location', 'branch_id', 'branch', 'id'),
    ForeignKey('location', 'address_id', 'address', 'id'),
    ForeignKey('location', 'aci_id', 'aci_data', 'id'),
    ForeignKey('location', 'contact_phone_id', 'phone', 'id'),
]

def createLocationTable(conn):
    locationTable = SqlTable('location', conn, locationFields, locationIndexes, locationForeignKeys)
    locationTable.createTable()
    locationTable.addIndexes()

    return locationTable

def addLocation(
    conn : Connection,
    branchId : int,
    companyName : str,
    locationName : str,
    addressId : int,
    aciId : int,
    contactFirstName : str,
    contactLastName : str,
    contactEmail : str,
    contactPhoneId : int,
    isCarrier : bool,
    isLocal : bool,
    isInternational : bool,
    defaultWaitTime : int,
    isActive : bool,
) -> int:
    locationRow = conn.sqlGetInfo('location', 'id', f"[branch_id] = '{branchId}' AND [company_name] = '{companyName}' AND [location_name] = '{locationName}' AND [address_id] = '{addressId}' AND [aci_id] = '{aciId}' AND [contact_first_name] = '{contactFirstName}' AND [contact_last_name] = '{contactLastName}' AND [contact_email] = '{contactEmail}' AND [contact_phone_id] = '{contactPhoneId}' AND [is_carrier] = '{isCarrier}' AND [is_local] = '{isLocal}' AND [is_international] = '{isInternational}' AND [default_wait_time] = '{defaultWaitTime}' AND [is_active] = '{isActive}'")
    if locationRow:
        return locationRow[0].id
    data = {
        'branch_id' : branchId,
        'company_name' : companyName,
        'location_name' : locationName,
        'address_id' : addressId,
        'aci_id' : aciId,
        'contact_first_name' : contactFirstName,
        'contact_last_name' : contactLastName,
        'contact_email' : contactEmail,
        'contact_phone_id' : contactPhoneId,
        'is_carrier' : isCarrier,
        'is_local' : isLocal,
        'is_international' : isInternational,
        'default_wait_time' : defaultWaitTime,
        'is_active' : isActive,
    }
    conn.sqlInsertRow('location', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('location')