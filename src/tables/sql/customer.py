from ...imports import *

customerFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="branch_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="customer_name", fieldDetails="NVARCHAR(63) NOT NULL"),
    Field(fieldName="address_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="phone_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="default_rate_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="fuel_service_charge", fieldDetails="MONEY NOT NULL"),
    Field(fieldName="qb_customer_ref_id", fieldDetails="NVARCHAR(127)"),
    Field(fieldName="qb_customer_ref_name", fieldDetails="NVARCHAR(127)"),
    Field(fieldName="is_qb_invoice_omitted", fieldDetails="BIT NOT NULL"),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL DEFAULT (1)"),
    Field(fieldName="notes", fieldDetails="NTEXT NOT NULL"),
]

customerIndexes: List[Index] = [
]

customerForeignKeys: List[ForeignKey] = [
    ForeignKey('customer', 'branch_id', 'branch', 'id'),
    ForeignKey('customer', 'address_id', 'address', 'id'),
    ForeignKey('customer', 'phone_id', 'phone', 'id'),
    ForeignKey('customer', 'default_rate_id', 'rate', 'id'),
]

def createCustomerTable(conn):
    customerTable = SqlTable('customer', conn, customerFields, customerIndexes, customerForeignKeys)
    customerTable.createTable()
    customerTable.addIndexes()

    return customerTable

def addCustomer(
    conn : Connection,
    customerId : int,
    branchId : int,
    customerName : str,
    addressId : int,
    phoneId : int,
    defaultRateId : int,
    fuelServiceCharge : float,
    qbCustomerRefId : str,
    qbCustomerRefName : str,
    isQbInvoiceOmitted : bool,
    isActive : bool,
    notes : bool,
) -> int:
    customerRow = conn.sqlGetInfo('customer', 'id', f"[branch_id] = '{branchId}' AND [customer_name] = '{customerName}' AND [address_id] = '{addressId}' AND [phone_id] = '{phoneId}' AND [default_rate_id] = '{defaultRateId}' AND [fuel_service_charge] = '{fuelServiceCharge}' AND [qb_customer_ref_id] = '{qbCustomerRefId}' AND [qb_customer_ref_name] = '{qbCustomerRefName}' AND [is_qb_invoice_omitted] = '{isQbInvoiceOmitted}' AND [is_active] = '{isActive}' AND [notes] = '{notes}'")
    if customerRow:
        return customerRow[0].id
    data = {
        'branch_id' : branchId,
        'customer_name' : customerName,
        'address_id' : addressId,
        'phone_id' : phoneId,
        'default_rate_id' : defaultRateId,
        'fuel_service_charge' : fuelServiceCharge,
        'qb_customer_ref_id' : qbCustomerRefId,
        'qb_customer_ref_name' : qbCustomerRefName,
        'is_qb_invoice_omitted' : isQbInvoiceOmitted,
        'is_active' : isActive,
        'notes' : notes,
    }
    conn.sqlInsertRow('customer', data, insertId=customerId)
    conn.commit()

    return conn.sqlGetLastIdCreated('customer')