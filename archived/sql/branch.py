from ...imports import *

branchFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="branch_name", fieldDetails="NVARCHAR(63) NOT NULL"),
    Field(fieldName="company_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="address_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="airport_code", fieldDetails="NVARCHAR(5) NOT NULL"),
    Field(fieldName="email", fieldDetails="NVARCHAR(127) NOT NULL"),
    Field(fieldName="phone_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="fax_id", fieldDetails="INTEGER"),
    Field(fieldName="cartage_agent_type", fieldDetails="NVARCHAR(15) NOT NULL DEFAULT 'cartage'"),
    Field(fieldName="fuel_service_charge", fieldDetails="MONEY NOT NULL"),
    Field(fieldName="transfer_rate", fieldDetails="MONEY NOT NULL"),
    Field(fieldName="international_air_dim_divisor", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="domestic_air_dim_divisor", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="truck_dim_divisor", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="aci_low", fieldDetails="NVARCHAR(1) NOT NULL"),
    Field(fieldName="aci_high", fieldDetails="NVARCHAR(1) NOT NULL"),
    Field(fieldName="notes", fieldDetails="NTEXT"),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL"),
]

branchIndexes: List[Index] = [
]

branchForeignKeys: List[ForeignKey] = [
    ForeignKey('branch', 'company_id', 'company', 'id'),
    ForeignKey('branch', 'phone_id', 'phone', 'id'),
    ForeignKey('branch', 'fax_id', 'fax', 'id'),
]

def createBranchTable(conn):
    branchTable = SqlTable('branch', conn, branchFields, branchIndexes, branchForeignKeys)
    branchTable.createTable()
    branchTable.addIndexes()

    return branchTable

def addBranch(
    conn : Connection,
    branchId : int,
    branchName : str,
    companyId : int,
    addressId : int,
    airportCode : str,
    email : str,
    phoneId : int,
    faxId : int,
    cartageAgentType : str,
    fuelServiceCharge : float,
    transferRate : float,
    internationalAirDimDivisor : int,
    domesticAirDimDivisor : int,
    truckDimDivisor : int,
    aciLow : str,
    aciHigh : str,
    notes : str,
    isActive : bool,
) -> int:
    branchRow = conn.sqlGetInfo(
      'branch',
      'id',
      whereDetails={
          'branch_name': branchName,
          'company_id': companyId,
          'address_id': addressId,
          'airport_code': airportCode,
          'email': email,
          'phone_id': phoneId,
          'fax_id': faxId,
          'cartage_agent_type': cartageAgentType,
          'fuel_service_charge': fuelServiceCharge,
          'transfer_rate': transferRate,
          'international_air_dim_divisor': internationalAirDimDivisor,
          'domestic_air_dim_divisor': domesticAirDimDivisor,
          'truck_dim_divisor': truckDimDivisor,
          'aci_low': aciLow,
          'aci_high': aciHigh,
          'notes': notes,
          'is_active': isActive
      }
    )
    if branchRow:
        return branchRow[0].id
    data = {
        'branch_name' : branchName,
        'company_id' : companyId,
        'address_id' : addressId,
        'airport_code' : airportCode,
        'email' : email,
        'phone_id' : phoneId,
        'fax_id' : faxId,
        'cartage_agent_type' : cartageAgentType,
        'fuel_service_charge' : fuelServiceCharge,
        'transfer_rate' : transferRate,
        'international_air_dim_divisor' : internationalAirDimDivisor,
        'domestic_air_dim_divisor' : domesticAirDimDivisor,
        'truck_dim_divisor' : truckDimDivisor,
        'aci_low' : aciLow,
        'aci_high' : aciHigh,
        'notes' : notes,
        'is_active' : isActive,
    }
    conn.sqlInsertRow('branch', data, insertId=branchId)
    conn.commit()

    return conn.sqlGetLastIdCreated('branch')