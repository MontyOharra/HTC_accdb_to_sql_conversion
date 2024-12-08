from ...imports import *

companyFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="company_name", fieldDetails="NVARCHAR(63) NOT NULL"),
    Field(fieldName="address_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="phone_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="airport_code", fieldDetails="NVARCHAR(5)"),
    Field(fieldName="fax_id", fieldDetails="INTEGER"),
    Field(fieldName="cartage_agent_type", fieldDetails="NVARCHAR(15) NOT NULL DEFAULT 'cartage'"),
    Field(fieldName="employer_identification_no", fieldDetails="NCHAR(10) UNIQUE NOT NULL"),
    Field(fieldName="email", fieldDetails="NVARCHAR(255) UNIQUE NOT NULL"),
    Field(fieldName="scac", fieldDetails="NVARCHAR(5) UNIQUE NOT NULL"),
    Field(fieldName="website", fieldDetails="NVARCHAR(511)"),
    Field(fieldName="notes", fieldDetails="NTEXT"),
    Field(fieldName="logo_path", fieldDetails="NVARCHAR(MAX)"),
    Field(fieldName="is_tsa_compliant", fieldDetails="BIT NOT NULL DEFAULT (0)"),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL DEFAULT (1)"),
]

companyIndexes: List[Index] = [
]

companyForeignKeys: List[ForeignKey] = [
    ForeignKey('company', 'address_id', 'address', 'id'),
    ForeignKey('company', 'phone_id', 'phone', 'id'),
    ForeignKey('company', 'fax_id', 'fax', 'id'),
]

def createCompanyTable(conn):
    companyTable = SqlTable('company', conn, companyFields, companyIndexes, companyForeignKeys)
    companyTable.createTable()
    companyTable.addIndexes()

    return companyTable

def addCompany(
    conn : Connection,
    companyName : str,
    addressId : int,
    phoneId : int,
    airportCode : str,
    faxId : int,
    cartageAgentType : str,
    employerIdentificationNo : str,
    email : str,
    scac : str,
    website : str,
    notes : str,
    logoPath : str,
    isTsaCompliant : bool,
    isActive : bool,
) -> int:
    data = {
        'company_name' : companyName,
        'address_id' : addressId,
        'phone_id' : phoneId,
        'airport_code' : airportCode,
        'fax_id' : faxId,
        'cartage_agent_type' : cartageAgentType,
        'employer_identification_no' : employerIdentificationNo,
        'email' : email,
        'scac' : scac,
        'website' : website,
        'notes' : notes,
        'logo_path' : logoPath,
        'is_tsa_compliant' : isTsaCompliant,
        'is_active' : isActive,
    }
    conn.sqlInsertRow('company', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('company')