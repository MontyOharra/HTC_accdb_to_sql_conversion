from ...imports import *

orderFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="branch_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="order_type_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="customer_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="agent_id", fieldDetails="INTEGER"),
    Field(fieldName="rate_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="hawb", fieldDetails="NVARCHAR(31)"),
    Field(fieldName="mawb", fieldDetails="NVARCHAR(31)"),
    Field(fieldName="order_notes", fieldDetails="NTEXT"),
    Field(fieldName="pu_time_start", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="pu_time_end", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="del_time_start", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="del_time_end", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="pu_location_id", fieldDetails="INTEGER"),
    Field(fieldName="pu_contact_phone_id", fieldDetails="INTEGER"),
    Field(fieldName="pu_contact_name", fieldDetails="NVARCHAR(63)"),
    Field(fieldName="pu_notes", fieldDetails="NTEXT"),
    Field(fieldName="del_location_id", fieldDetails="INTEGER"),
    Field(fieldName="del_contact_phone_id", fieldDetails="INTEGER"),
    Field(fieldName="del_contact_name", fieldDetails="NVARCHAR(63)"),
    Field(fieldName="del_notes", fieldDetails="NTEXT"),
    Field(fieldName="driver_name", fieldDetails="NVARCHAR(63)"),
    Field(fieldName="pod_signee", fieldDetails="NVARCHAR(63)"),
    Field(fieldName="pod_time_signed", fieldDetails="DATETIME2"),
    Field(fieldName="pod_notes", fieldDetails="NTEXT"),
    Field(fieldName="status_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="rating_weight_charges", fieldDetails="MONEY"),
    Field(fieldName="rating_fuel_charges", fieldDetails="MONEY"),
    Field(fieldName="rating_service_charges", fieldDetails="MONEY"),
    Field(fieldName="rating_total_charges", fieldDetails="MONEY"),
    Field(fieldName="rating_total_expenses", fieldDetails="MONEY"),
    Field(fieldName="rating_storage_charges", fieldDetails="MONEY"),
    Field(fieldName="rating_adjustments", fieldDetails="MONEY"),
    Field(fieldName="rating_notes", fieldDetails="NTEXT"),
    Field(fieldName="quickbooks_customer_list_id", fieldDetails="NVARCHAR(50)"),
    Field(fieldName="quickbooks_customer_name", fieldDetails="NVARCHAR(50)"),
    Field(fieldName="quickbooks_invoice_reference_number", fieldDetails="NVARCHAR(50)"),
    Field(fieldName="quickbooks_line_sequence_number", fieldDetails="NVARCHAR(50)"),
    Field(fieldName="is_auto_assessorials", fieldDetails="BIT"),
    Field(fieldName="is_weight_charge_calculated", fieldDetails="BIT"),
]

orderIndexes: List[Index] = [
]

orderForeignKeys: List[ForeignKey] = [
    ForeignKey('order', 'branch_id', 'branch', 'id'),
    ForeignKey('order', 'order_type_id', 'order_type', 'id'),
    ForeignKey('order', 'customer_id', 'customer', 'id'),
    ForeignKey('order', 'agent_id', 'agent', 'id'),
    ForeignKey('order', 'rate_id', 'rate', 'id'),
    ForeignKey('order', 'pu_location_id', 'location', 'id'),
    ForeignKey('order', 'pu_contact_phone_id', 'phone', 'id'),
    ForeignKey('order', 'del_location_id', 'location', 'id'),
    ForeignKey('order', 'del_contact_phone_id', 'phone', 'id'),
    ForeignKey('order', 'status_id', 'order_status', 'id'),
]

def createOrderTable(conn):
    orderTable = SqlTable('order', conn, orderFields, orderIndexes, orderForeignKeys)
    orderTable.createTable()
    orderTable.addIndexes()

    return orderTable

def addOrder(
    conn : Connection,
    orderId : int,
    branchId : int,
    orderTypeId : int,
    customerId : int,
    agentId : int,
    rateId : int,
    hawb : str,
    mawb : str,
    orderNotes : str,
    puTimeStart : str,
    puTimeEnd : str,
    delTimeStart : str,
    delTimeEnd : str,
    puLocationId : int,
    puContactPhoneId : int,
    puContactName : str,
    puNotes : str,
    delLocationId : int,
    delContactPhoneId : int,
    delContactName : str,
    delNotes : str,
    driverName : str,
    podSignee : str,
    podTimeSigned : str,
    podNotes : str,
    statusId : int,
    ratingWeightCharges : float,
    ratingFuelCharges : float,
    ratingServiceCharges : float,
    ratingTotalCharges : float,
    ratingTotalExpenses : float,
    ratingStorageCharges : float,
    ratingAdjustments : float,
    ratingNotes : float,
    quickbooksCustomerListId : str,
    quickbooksCustomerName : str,
    quickbooksInvoiceReferenceNumber : str,
    quickbooksLineSequenceNumber : str,
    isAutoAssessorials : bool,
    isWeightChargeCalculated : bool,
) -> int:
    orderRow = conn.sqlGetInfo('order', 'id', f"[branch_id] = '{branchId}' AND [order_type_id] = '{orderTypeId}' AND [customer_id] = '{customerId}' AND [agent_id] = '{agentId}' AND [rate_id] = '{rateId}' AND [hawb] = '{hawb}' AND [mawb] = '{mawb}' AND [order_notes] = '{orderNotes}' AND [pu_time_start] = '{puTimeStart}' AND [pu_time_end] = '{puTimeEnd}' AND [del_time_start] = '{delTimeStart}' AND [del_time_end] = '{delTimeEnd}' AND [pu_location_id] = '{puLocationId}' AND [pu_contact_phone_id] = '{puContactPhoneId}' AND [pu_contact_name] = '{puContactName}' AND [pu_notes] = '{puNotes}' AND [del_location_id] = '{delLocationId}' AND [del_contact_phone_id] = '{delContactPhoneId}' AND [del_contact_name] = '{delContactName}' AND [del_notes] = '{delNotes}' AND [driver_name] = '{driverName}' AND [pod_signee] = '{podSignee}' AND [pod_time_signed] = '{podTimeSigned}' AND [pod_notes] = '{podNotes}' AND [status_id] = '{statusId}' AND [rating_weight_charges] = '{ratingWeightCharges}' AND [rating_fuel_charges] = '{ratingFuelCharges}' AND [rating_service_charges] = '{ratingServiceCharges}' AND [rating_total_charges] = '{ratingTotalCharges}' AND [rating_total_expenses] = '{ratingTotalExpenses}' AND [rating_storage_charges] = '{ratingStorageCharges}' AND [rating_adjustments] = '{ratingAdjustments}' AND [rating_notes] = '{ratingNotes}' AND [quickbooks_customer_list_id] = '{quickbooksCustomerListId}' AND [quickbooks_customer_name] = '{quickbooksCustomerName}' AND [quickbooks_invoice_reference_number] = '{quickbooksInvoiceReferenceNumber}' AND [quickbooks_line_sequence_number] = '{quickbooksLineSequenceNumber}' AND [is_auto_assessorials] = '{isAutoAssessorials}' AND [is_weight_charge_calculated] = '{isWeightChargeCalculated}'")
    if orderRow:
        return orderRow[0].id
    data = {
        'branch_id' : branchId,
        'order_type_id' : orderTypeId,
        'customer_id' : customerId,
        'agent_id' : agentId,
        'rate_id' : rateId,
        'hawb' : hawb,
        'mawb' : mawb,
        'order_notes' : orderNotes,
        'pu_time_start' : puTimeStart,
        'pu_time_end' : puTimeEnd,
        'del_time_start' : delTimeStart,
        'del_time_end' : delTimeEnd,
        'pu_location_id' : puLocationId,
        'pu_contact_phone_id' : puContactPhoneId,
        'pu_contact_name' : puContactName,
        'pu_notes' : puNotes,
        'del_location_id' : delLocationId,
        'del_contact_phone_id' : delContactPhoneId,
        'del_contact_name' : delContactName,
        'del_notes' : delNotes,
        'driver_name' : driverName,
        'pod_signee' : podSignee,
        'pod_time_signed' : podTimeSigned,
        'pod_notes' : podNotes,
        'status_id' : statusId,
        'rating_weight_charges' : ratingWeightCharges,
        'rating_fuel_charges' : ratingFuelCharges,
        'rating_service_charges' : ratingServiceCharges,
        'rating_total_charges' : ratingTotalCharges,
        'rating_total_expenses' : ratingTotalExpenses,
        'rating_storage_charges' : ratingStorageCharges,
        'rating_adjustments' : ratingAdjustments,
        'rating_notes' : ratingNotes,
        'quickbooks_customer_list_id' : quickbooksCustomerListId,
        'quickbooks_customer_name' : quickbooksCustomerName,
        'quickbooks_invoice_reference_number' : quickbooksInvoiceReferenceNumber,
        'quickbooks_line_sequence_number' : quickbooksLineSequenceNumber,
        'is_auto_assessorials' : isAutoAssessorials,
        'is_weight_charge_calculated' : isWeightChargeCalculated,
    }
    conn.sqlInsertRow('order', data, insertId=orderId)
    conn.commit()

    return conn.sqlGetLastIdCreated('order')