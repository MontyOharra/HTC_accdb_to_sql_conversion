from ...imports import *

aciDataChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="aci_data_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="user_id", fieldDetails="INTEGER"),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL"),
]

aciDataFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="city_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="postal_code_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="airport_code", fieldDetails="NVARCHAR(5)"),
    Field(fieldName="carrier", fieldDetails="NVARCHAR(50) DEFAULT ''"),
    Field(fieldName="area", fieldDetails="NVARCHAR(1)"),
    Field(fieldName="rate_min", fieldDetails="MONEY"),
    Field(fieldName="rate_100", fieldDetails="MONEY"),
    Field(fieldName="rate_1000", fieldDetails="MONEY"),
    Field(fieldName="rate_2000", fieldDetails="MONEY"),
    Field(fieldName="rate_5000", fieldDetails="MONEY"),
    Field(fieldName="date_created", fieldDetails="DATETIME2"),
    Field(fieldName="created_by", fieldDetails="INTEGER"),
    Field(fieldName="branch_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL DEFAULT (1)"),
]

addressFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="address_line_1", fieldDetails="NVARCHAR(127) NOT NULL"),
    Field(fieldName="address_line_2", fieldDetails="NVARCHAR(63)"),
    Field(fieldName="city_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="postal_code_id", fieldDetails="INTEGER NOT NULL"),
]

agentCertificationTestFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="agent_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="certification_test_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="date_tested", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="test_score", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL DEFAULT (1)"),
]

agentChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="agent_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="user_id", fieldDetails="INTEGER"),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL"),
]

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

archiveErrorLogFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="order_id", fieldDetails="INTEGER"),
    Field(fieldName="archive_date", fieldDetails="DATETIME2"),
    Field(fieldName="user_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="details", fieldDetails="NTEXT"),
]

archiveHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="date_archived", fieldDetails="DATETIME2"),
    Field(fieldName="open_orders", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="open_order_assessorials", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="open_order_dimensions", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="open_order_drivers", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="open_order_attachments", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="invoiced_orders", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="invoiced_order_assessorials", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="invoiced_order_dimensions", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="invoiced_order_drivers", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="invoiced_order_attachments", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="remaining_orders", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="remaining_order_assessorials", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="remaining_order_dimensions", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="remaining_order_drivers", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="remaining_order_attachments", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="dock_orders", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="dock_order_assessorials", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="dock_order_dimensions", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="dock_order_drivers", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="dock_order_attachments", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="service_orders", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="service_order_assessorials", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="service_order_dimensions", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="service_order_drivers", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="service_order_attachments", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="active_order_history", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="active_order_hawbs", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="archived_orders", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="archived_order_assessorials", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="archived_order_dimensions", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="archived_order_drivers", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="archived_order_attachments", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="archived_order_history", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="archived_order_hawbs", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="removed_orders", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="removed_order_assessorials", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="removed_order_dimensions", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="removed_order_drivers", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="removed_order_attachments", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="removed_order_history", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="removed_order_hawbs", fieldDetails="INTEGER DEFAULT (0)"),
]

assessorialChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="assessorial_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="user_id", fieldDetails="INTEGER"),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL"),
]

assessorialFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="branch_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="assessorial_name", fieldDetails="NVARCHAR(127) NOT NULL"),
    Field(fieldName="min_charge", fieldDetails="MONEY NOT NULL"),
    Field(fieldName="basis_type", fieldDetails="nvarchar(255) NOT NULL CHECK ([basis_type] IN ('fixed', 'weight', 'prompt'))"),
    Field(fieldName="basis_portion", fieldDetails="FLOAT NOT NULL"),
    Field(fieldName="basis_rate", fieldDetails="MONEY"),
    Field(fieldName="user_prompt", fieldDetails="NVARCHAR(127)"),
    Field(fieldName="date_created", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="notes", fieldDetails="NTEXT"),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL DEFAULT (1)"),
]

branchChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="branch_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="user_id", fieldDetails="INTEGER"),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="changes", fieldDetails="NTEXT"),
]

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

certificationTestFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="certification_name", fieldDetails="NVARCHAR(63) NOT NULL"),
    Field(fieldName="certification_test_trainer_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL"),
]

certificationTestChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="certification_test_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="user_id", fieldDetails="INTEGER"),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL"),
]

certificationTestTrainerFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="trainer_name", fieldDetails="NVARCHAR(63)"),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL DEFAULT (1)"),
]

certificationTestTrainerChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="certification_test_trainer_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="user_id", fieldDetails="INTEGER"),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL"),
]

cityPostalCodeFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="city_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="postal_code_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="lat", fieldDetails="DECIMAL NOT NULL"),
    Field(fieldName="lng", fieldDetails="DECIMAL NOT NULL"),
]

cityRegionFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="city_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="region_id", fieldDetails="INTEGER NOT NULL"),
]


cityFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="city_name", fieldDetails="NVARCHAR(63) NOT NULL"),
]

companyChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="company_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="user_id", fieldDetails="INTEGER"),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL"),
]

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
    
countryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="country_name", fieldDetails="NVARCHAR(63) UNIQUE NOT NULL"),
    Field(fieldName="iso_code_2", fieldDetails="NVARCHAR(2) UNIQUE NOT NULL"),
    Field(fieldName="iso_code_3", fieldDetails="NVARCHAR(3) UNIQUE NOT NULL"),
]

customerChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="customer_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="user_id", fieldDetails="INTEGER"),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL"),
]

customerDefaultAssessorialFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="customer_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="assessorial_id", fieldDetails="INTEGER NOT NULL"),
]

customerFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="branch_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="customer_name", fieldDetails="NVARCHAR(63) NOT NULL"),
    Field(fieldName="address_id", fieldDetails="INTEGER"),
    Field(fieldName="phone_id", fieldDetails="INTEGER"),
    Field(fieldName="default_rate_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="fuel_service_charge", fieldDetails="MONEY NOT NULL"),
    Field(fieldName="qb_customer_ref_id", fieldDetails="NVARCHAR(127)"),
    Field(fieldName="qb_customer_ref_name", fieldDetails="NVARCHAR(127)"),
    Field(fieldName="is_qb_invoice_omitted", fieldDetails="BIT NOT NULL"),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL DEFAULT (1)"),
    Field(fieldName="notes", fieldDetails="NTEXT"),
]

faxFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="country_code", fieldDetails="NVARCHAR(3) NOT NULL"),
    Field(fieldName="area_code", fieldDetails="NVARCHAR(5) NOT NULL"),
    Field(fieldName="fax_number", fieldDetails="NVARCHAR(14) NOT NULL"),
    Field(fieldName="fax_extension", fieldDetails="NVARCHAR(4)"),
]

holidayFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="holiday_name", fieldDetails="NVARCHAR(31) NOT NULL"),
    Field(fieldName="holiday_date", fieldDetails="DATETIME2 NOT NULL"),
]

locationChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="location_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="user_id", fieldDetails="INTEGER"),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL"),
]

locationDefaultAssessorialFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="location_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="assessorial_id", fieldDetails="INTEGER NOT NULL"),
]

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

orderAssessorialFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="order_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="assessorial_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="parent_type", fieldDetails="NVARCHAR(15) NOT NULL"),
    Field(fieldName="basis_count", fieldDetails="DECIMAL(6,2)"),
    Field(fieldName="total_charge", fieldDetails="MONEY"),
]

orderAttachmentFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="order_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="attachment_path", fieldDetails="NVARCHAR(MAX)"),
    Field(fieldName="file_size", fieldDetails="DECIMAL(30,15)"),
]

orderChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="order_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="user_id", fieldDetails="INTEGER"),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL"),
]

orderDimFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="order_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="unit_type", fieldDetails="NVARCHAR(15)"),
    Field(fieldName="unit_quantity", fieldDetails="INTEGER"),
    Field(fieldName="unit_weight", fieldDetails="INTEGER"),
    Field(fieldName="dim_height", fieldDetails="INTEGER"),
    Field(fieldName="dim_width", fieldDetails="INTEGER"),
    Field(fieldName="dim_length", fieldDetails="INTEGER"),
    Field(fieldName="dim_weight", fieldDetails="DECIMAL(20,10)"),
]

orderDriverFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="order_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="driver_user_id", fieldDetails="INTEGER"),
    Field(fieldName="order_leg", fieldDetails="NVARCHAR(1)"),
    Field(fieldName="driver_role", fieldDetails="NVARCHAR(1)"),
]

orderStatusChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="order_status_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="user_id", fieldDetails="INTEGER"),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL"),
]

orderStatusFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="order_status_name", fieldDetails="NVARCHAR(25) NOT NULL"),
    Field(fieldName="sequence_number", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="is_on_manifest", fieldDetails="BIT NOT NULL"),
    Field(fieldName="is_set_to_auto_notify", fieldDetails="BIT NOT NULL"),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL"),
    Field(fieldName="branch_id", fieldDetails="INTEGER NOT NULL"),
]

orderTypeFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="order_type_name", fieldDetails="NVARCHAR(31) NOT NULL"),
]

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
    Field(fieldName="pu_time_start", fieldDetails="DATETIME2"),
    Field(fieldName="pu_time_end", fieldDetails="DATETIME2"),
    Field(fieldName="del_time_start", fieldDetails="DATETIME2"),
    Field(fieldName="del_time_end", fieldDetails="DATETIME2"),
    Field(fieldName="pu_location_id", fieldDetails="INTEGER"),
    Field(fieldName="pu_notes", fieldDetails="NTEXT"),
    Field(fieldName="del_location_id", fieldDetails="INTEGER"),
    Field(fieldName="del_notes", fieldDetails="NTEXT"),
    Field(fieldName="driver_name", fieldDetails="NVARCHAR(63)"),
    Field(fieldName="pod_signee", fieldDetails="NVARCHAR(255)"),
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

overnightMaintenanceHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="date_overnight_maintenance", fieldDetails="DATETIME2"),
    Field(fieldName="user_id", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="open_orders_in", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="open_order_assessorials_in", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="open_order_dimensions_in", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="open_order_drivers_in", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="open_order_attachments_in", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="invoiced_orders_in", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="invoiced_order_assessorials_in", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="invoiced_order_dimensions_in", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="invoiced_order_drivers_in", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="invoiced_order_attachments_in", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="remaining_orders_in", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="remaining_order_assessorials_in", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="remaining_order_dimensions_in", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="remaining_order_drivers_in", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="remaining_order_attachments_in", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="open_orders_out", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="open_order_assessorials_out", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="open_order_dimensions_out", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="open_order_drivers_out", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="open_order_attachments_out", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="invoiced_orders_out", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="invoiced_order_assessorials_out", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="invoiced_order_dimensions_out", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="invoiced_order_drivers_out", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="invoiced_order_attachments_out", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="remaining_orders_out", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="remaining_order_assessorials_out", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="remaining_order_dimensions_out", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="remaining_order_drivers_out", fieldDetails="INTEGER DEFAULT (0)"),
    Field(fieldName="remaining_order_attachments_out", fieldDetails="INTEGER DEFAULT (0)"),
]

phoneFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="country_code", fieldDetails="NVARCHAR(3) NOT NULL"),
    Field(fieldName="area_code", fieldDetails="NVARCHAR(5) NOT NULL"),
    Field(fieldName="phone_number", fieldDetails="NVARCHAR(14) NOT NULL"),
    Field(fieldName="phone_extension", fieldDetails="NVARCHAR(4)"),
]

positionChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="position_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="user_id", fieldDetails="INTEGER"),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL"),
]

positionFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="position_name", fieldDetails="NVARCHAR(35) NOT NULL"),
    Field(fieldName="security_level", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL"),
    Field(fieldName="branch_id", fieldDetails="INTEGER NOT NULL"),
]

postalCodeRegionFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="postal_code_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="region_id", fieldDetails="INTEGER NOT NULL"),
]

postalCodeFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="postal_code", fieldDetails="NVARCHAR(15) NOT NULL"),
]

rateAreaFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="rate_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="area", fieldDetails="NVARCHAR(1) NOT NULL"),
    Field(fieldName="rate_min", fieldDetails="MONEY"),
    Field(fieldName="rate_100", fieldDetails="MONEY"),
    Field(fieldName="rate_1000", fieldDetails="MONEY"),
    Field(fieldName="rate_2000", fieldDetails="MONEY"),
    Field(fieldName="rate_5000", fieldDetails="MONEY"),
    Field(fieldName="rate_max", fieldDetails="MONEY"),
]

rateChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="rate_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="user_id", fieldDetails="INTEGER"),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL"),
]

rateFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="rate_name", fieldDetails="NVARCHAR(31) NOT NULL"),
    Field(fieldName="branch_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="is_default", fieldDetails="BIT NOT NULL DEFAULT (0)"),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL DEFAULT (1)"),
    Field(fieldName="date_added", fieldDetails="DATETIME2"),
    Field(fieldName="added_by_user_id", fieldDetails="INTEGER"),
]
    
regionFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="country_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="iso_code", fieldDetails="NVARCHAR(6) NOT NULL"),
    Field(fieldName="region_name", fieldDetails="NVARCHAR(63) NOT NULL"),
]

specialChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="special_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="user_id", fieldDetails="INTEGER"),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL"),
]

specialFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="old_id", fieldDetails="INTEGER"),
    Field(fieldName="branch_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="weekday", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="start_time", fieldDetails="TIME NOT NULL"),
    Field(fieldName="end_time", fieldDetails="TIME NOT NULL"),
    Field(fieldName="area", fieldDetails="NVARCHAR(1) NOT NULL"),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL DEFAULT (1)"),
]

userChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="user_changed_id", fieldDetails="INTEGER NOT NULL"),
    Field(fieldName="user_id", fieldDetails="INTEGER"),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL"),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL"),
]

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
