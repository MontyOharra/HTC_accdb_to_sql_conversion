from typing import List
from src.types import Field

aciDataChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="aci_data_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="user_id", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL", isPrimaryKey=False),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL", isPrimaryKey=False),
]

aciDataFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="city_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="postal_code_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="airport_code", fieldDetails="NVARCHAR(5)", isPrimaryKey=False),
    Field(fieldName="carrier", fieldDetails="NVARCHAR(50) DEFAULT ''", isPrimaryKey=False),
    Field(fieldName="area", fieldDetails="NVARCHAR(1)", isPrimaryKey=False),
    Field(fieldName="rate_min", fieldDetails="MONEY", isPrimaryKey=False),
    Field(fieldName="rate_100", fieldDetails="MONEY", isPrimaryKey=False),
    Field(fieldName="rate_1000", fieldDetails="MONEY", isPrimaryKey=False),
    Field(fieldName="rate_2000", fieldDetails="MONEY", isPrimaryKey=False),
    Field(fieldName="rate_5000", fieldDetails="MONEY", isPrimaryKey=False),
    Field(fieldName="date_created", fieldDetails="DATETIME2", isPrimaryKey=False),
    Field(fieldName="created_by", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="branch_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL DEFAULT (1)", isPrimaryKey=False),
]

addressFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="address_line_1", fieldDetails="NVARCHAR(127) NOT NULL", isPrimaryKey=False),
    Field(fieldName="address_line_2", fieldDetails="NVARCHAR(63)", isPrimaryKey=False),
    Field(fieldName="city_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="postal_code_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="lat", fieldDetails="FLOAT", isPrimaryKey=False),
    Field(fieldName="lng", fieldDetails="FLOAT", isPrimaryKey=False),
]

agentCertificationTestFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="agent_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="certification_test_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="date_tested", fieldDetails="DATETIME2 NOT NULL", isPrimaryKey=False),
    Field(fieldName="test_score", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL DEFAULT (1)", isPrimaryKey=False),
]

agentChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="agent_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="user_id", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL", isPrimaryKey=False),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL", isPrimaryKey=False),
]

agentFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="customer_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="email_address", fieldDetails="NVARCHAR(127) NOT NULL", isPrimaryKey=False),
    Field(fieldName="first_name", fieldDetails="NVARCHAR(50)", isPrimaryKey=False),
    Field(fieldName="last_name", fieldDetails="NVARCHAR(50)", isPrimaryKey=False),
    Field(fieldName="phone_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="mobile_phone_id", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="fax_id", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="is_set_to_auto_notify_email", fieldDetails="BIT NOT NULL DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL DEFAULT (1)", isPrimaryKey=False),
]

archiveErrorLogFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="order_id", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="archive_date", fieldDetails="DATETIME2", isPrimaryKey=False),
    Field(fieldName="user_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="details", fieldDetails="NTEXT", isPrimaryKey=False),
]

archiveHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="date_archived", fieldDetails="DATETIME2", isPrimaryKey=False),
    Field(fieldName="open_orders", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="open_order_assessorials", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="open_order_dimensions", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="open_order_drivers", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="open_order_attachments", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="invoiced_orders", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="invoiced_order_assessorials", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="invoiced_order_dimensions", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="invoiced_order_drivers", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="invoiced_order_attachments", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="remaining_orders", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="remaining_order_assessorials", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="remaining_order_dimensions", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="remaining_order_drivers", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="remaining_order_attachments", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="dock_orders", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="dock_order_assessorials", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="dock_order_dimensions", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="dock_order_drivers", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="dock_order_attachments", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="service_orders", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="service_order_assessorials", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="service_order_dimensions", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="service_order_drivers", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="service_order_attachments", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="active_order_history", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="active_order_hawbs", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="archived_orders", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="archived_order_assessorials", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="archived_order_dimensions", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="archived_order_drivers", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="archived_order_attachments", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="archived_order_history", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="archived_order_hawbs", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="removed_orders", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="removed_order_assessorials", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="removed_order_dimensions", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="removed_order_drivers", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="removed_order_attachments", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="removed_order_history", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="removed_order_hawbs", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
]

assessorialChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="assessorial_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="user_id", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL", isPrimaryKey=False),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL", isPrimaryKey=False),
]

assessorialFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="branch_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="assessorial_name", fieldDetails="NVARCHAR(127) NOT NULL", isPrimaryKey=False),
    Field(fieldName="min_charge", fieldDetails="MONEY NOT NULL", isPrimaryKey=False),
    Field(fieldName="basis_type", fieldDetails="nvarchar(255) NOT NULL CHECK ([basis_type] IN ('fixed', 'weight', 'prompt'))", isPrimaryKey=False),
    Field(fieldName="basis_portion", fieldDetails="FLOAT NOT NULL", isPrimaryKey=False),
    Field(fieldName="basis_rate", fieldDetails="MONEY", isPrimaryKey=False),
    Field(fieldName="user_prompt", fieldDetails="NVARCHAR(127)", isPrimaryKey=False),
    Field(fieldName="date_created", fieldDetails="DATETIME2 NOT NULL", isPrimaryKey=False),
    Field(fieldName="notes", fieldDetails="NTEXT", isPrimaryKey=False),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL DEFAULT (1)", isPrimaryKey=False),
]

branchChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="branch_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="user_id", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL", isPrimaryKey=False),
    Field(fieldName="changes", fieldDetails="NTEXT", isPrimaryKey=False),
]

branchFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="branch_name", fieldDetails="NVARCHAR(63) NOT NULL", isPrimaryKey=False),
    Field(fieldName="company_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="address_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="airport_code", fieldDetails="NVARCHAR(5) NOT NULL", isPrimaryKey=False),
    Field(fieldName="email", fieldDetails="NVARCHAR(127) NOT NULL", isPrimaryKey=False),
    Field(fieldName="phone_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="fax_id", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="cartage_agent_type", fieldDetails="NVARCHAR(15) NOT NULL DEFAULT 'cartage'", isPrimaryKey=False),
    Field(fieldName="fuel_service_charge", fieldDetails="MONEY NOT NULL", isPrimaryKey=False),
    Field(fieldName="transfer_rate", fieldDetails="MONEY NOT NULL", isPrimaryKey=False),
    Field(fieldName="international_air_dim_divisor", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="domestic_air_dim_divisor", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="truck_dim_divisor", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="aci_low", fieldDetails="NVARCHAR(1) NOT NULL", isPrimaryKey=False),
    Field(fieldName="aci_high", fieldDetails="NVARCHAR(1) NOT NULL", isPrimaryKey=False),
    Field(fieldName="notes", fieldDetails="NTEXT", isPrimaryKey=False),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL", isPrimaryKey=False),
]

certificationTestFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="certification_name", fieldDetails="NVARCHAR(63) NOT NULL", isPrimaryKey=False),
    Field(fieldName="certification_test_trainer_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL", isPrimaryKey=False),
]

certificationTestChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="certification_test_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="user_id", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL", isPrimaryKey=False),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL", isPrimaryKey=False),
]

certificationTestTrainerFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="trainer_name", fieldDetails="NVARCHAR(63)", isPrimaryKey=False),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL DEFAULT (1)", isPrimaryKey=False),
]

certificationTestTrainerChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="certification_test_trainer_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="user_id", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL", isPrimaryKey=False),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL", isPrimaryKey=False),
]

cityPostalCodeFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="city_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="postal_code_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="lat", fieldDetails="DECIMAL NOT NULL", isPrimaryKey=False),
    Field(fieldName="lng", fieldDetails="DECIMAL NOT NULL", isPrimaryKey=False),
]

cityRegionFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="city_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="region_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
]

cityFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="city_name", fieldDetails="NVARCHAR(63) NOT NULL", isPrimaryKey=False),
    Field(fieldName="lat", fieldDetails="FLOAT", isPrimaryKey=False),
    Field(fieldName="lng", fieldDetails="FLOAT", isPrimaryKey=False),
]

companyChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="company_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="user_id", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL", isPrimaryKey=False),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL", isPrimaryKey=False),
]

companyFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="company_name", fieldDetails="NVARCHAR(63) NOT NULL", isPrimaryKey=False),
    Field(fieldName="address_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="phone_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="airport_code", fieldDetails="NVARCHAR(5)", isPrimaryKey=False),
    Field(fieldName="fax_id", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="cartage_agent_type", fieldDetails="NVARCHAR(15) NOT NULL DEFAULT 'cartage'", isPrimaryKey=False),
    Field(fieldName="employer_identification_no", fieldDetails="NCHAR(10) UNIQUE NOT NULL", isPrimaryKey=False),
    Field(fieldName="email", fieldDetails="NVARCHAR(255) UNIQUE NOT NULL", isPrimaryKey=False),
    Field(fieldName="scac", fieldDetails="NVARCHAR(5) UNIQUE NOT NULL", isPrimaryKey=False),
    Field(fieldName="website", fieldDetails="NVARCHAR(511)", isPrimaryKey=False),
    Field(fieldName="notes", fieldDetails="NTEXT", isPrimaryKey=False),
    Field(fieldName="logo_path", fieldDetails="NVARCHAR(MAX)", isPrimaryKey=False),
    Field(fieldName="is_tsa_compliant", fieldDetails="BIT NOT NULL DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL DEFAULT (1)", isPrimaryKey=False),
]
    
countryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=False),
    Field(fieldName="country_name", fieldDetails="NVARCHAR(63) NOT NULL", isPrimaryKey=False),
    Field(fieldName="iso_code_2", fieldDetails="NVARCHAR(2) NOT NULL", isPrimaryKey=False),
    Field(fieldName="iso_code_3", fieldDetails="NVARCHAR(3) NOT NULL", isPrimaryKey=False),
]

customerChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="customer_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="user_id", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL", isPrimaryKey=False),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL", isPrimaryKey=False),
]

customerDefaultAssessorialFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="customer_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="assessorial_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
]

customerFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="branch_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="customer_name", fieldDetails="NVARCHAR(63) NOT NULL", isPrimaryKey=False),
    Field(fieldName="address_id", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="phone_id", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="default_rate_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="fuel_service_charge", fieldDetails="MONEY NOT NULL", isPrimaryKey=False),
    Field(fieldName="qb_customer_ref_id", fieldDetails="NVARCHAR(127)", isPrimaryKey=False),
    Field(fieldName="qb_customer_ref_name", fieldDetails="NVARCHAR(127)", isPrimaryKey=False),
    Field(fieldName="is_qb_invoice_omitted", fieldDetails="BIT NOT NULL", isPrimaryKey=False),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL DEFAULT (1)", isPrimaryKey=False),
    Field(fieldName="notes", fieldDetails="NTEXT", isPrimaryKey=False),
]

faxFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="country_code", fieldDetails="NVARCHAR(3) NOT NULL", isPrimaryKey=False),
    Field(fieldName="area_code", fieldDetails="NVARCHAR(5) NOT NULL", isPrimaryKey=False),
    Field(fieldName="fax_number", fieldDetails="NVARCHAR(14) NOT NULL", isPrimaryKey=False),
    Field(fieldName="fax_extension", fieldDetails="NVARCHAR(4)", isPrimaryKey=False),
]

holidayFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="holiday_name", fieldDetails="NVARCHAR(31) NOT NULL", isPrimaryKey=False),
    Field(fieldName="holiday_date", fieldDetails="DATETIME2 NOT NULL", isPrimaryKey=False),
]

locationChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="location_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="user_id", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL", isPrimaryKey=False),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL", isPrimaryKey=False),
]

locationDefaultAssessorialFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="location_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="assessorial_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
]

locationFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="branch_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="company_name", fieldDetails="NVARCHAR(127)", isPrimaryKey=False),
    Field(fieldName="location_name", fieldDetails="NVARCHAR(127)", isPrimaryKey=False),
    Field(fieldName="address_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="aci_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="contact_first_name", fieldDetails="NVARCHAR(31)", isPrimaryKey=False),
    Field(fieldName="contact_last_name", fieldDetails="NVARCHAR(31)", isPrimaryKey=False),
    Field(fieldName="contact_email", fieldDetails="NVARCHAR(127)", isPrimaryKey=False),
    Field(fieldName="contact_phone_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="is_carrier", fieldDetails="BIT NOT NULL DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="is_local", fieldDetails="BIT NOT NULL DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="is_international", fieldDetails="BIT NOT NULL DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="default_wait_time", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL DEFAULT (1)", isPrimaryKey=False),
]

orderAssessorialFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="order_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="assessorial_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="parent_type", fieldDetails="NVARCHAR(15) NOT NULL", isPrimaryKey=False),
    Field(fieldName="basis_count", fieldDetails="DECIMAL(6,2)", isPrimaryKey=False),
    Field(fieldName="total_charge", fieldDetails="MONEY", isPrimaryKey=False),
]

orderAttachmentFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="order_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="attachment_path", fieldDetails="NVARCHAR(MAX)", isPrimaryKey=False),
    Field(fieldName="file_size", fieldDetails="DECIMAL(30,15)", isPrimaryKey=False),
]

orderChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="order_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="user_id", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL", isPrimaryKey=False),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL", isPrimaryKey=False),
]

orderDimFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="order_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="unit_type", fieldDetails="NVARCHAR(15)", isPrimaryKey=False),
    Field(fieldName="unit_quantity", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="unit_weight", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="dim_height", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="dim_width", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="dim_length", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="dim_weight", fieldDetails="DECIMAL(20,10)", isPrimaryKey=False),
]

orderDriverFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="order_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="driver_user_id", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="order_leg", fieldDetails="NVARCHAR(1)", isPrimaryKey=False),
    Field(fieldName="driver_role", fieldDetails="NVARCHAR(1)", isPrimaryKey=False),
]

orderStatusChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="order_status_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="user_id", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL", isPrimaryKey=False),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL", isPrimaryKey=False),
]

orderStatusFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="order_status_name", fieldDetails="NVARCHAR(25) NOT NULL", isPrimaryKey=False),
    Field(fieldName="sequence_number", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="is_on_manifest", fieldDetails="BIT NOT NULL", isPrimaryKey=False),
    Field(fieldName="is_set_to_auto_notify", fieldDetails="BIT NOT NULL", isPrimaryKey=False),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL", isPrimaryKey=False),
    Field(fieldName="branch_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
]

orderTypeFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="order_type_name", fieldDetails="NVARCHAR(31) NOT NULL", isPrimaryKey=False),
]

orderFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="branch_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="order_type_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="customer_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="agent_id", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="rate_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="hawb", fieldDetails="NVARCHAR(31)", isPrimaryKey=False),
    Field(fieldName="mawb", fieldDetails="NVARCHAR(31)", isPrimaryKey=False),
    Field(fieldName="order_notes", fieldDetails="NTEXT", isPrimaryKey=False),
    Field(fieldName="pu_time_start", fieldDetails="DATETIME2", isPrimaryKey=False),
    Field(fieldName="pu_time_end", fieldDetails="DATETIME2", isPrimaryKey=False),
    Field(fieldName="del_time_start", fieldDetails="DATETIME2", isPrimaryKey=False),
    Field(fieldName="del_time_end", fieldDetails="DATETIME2", isPrimaryKey=False),
    Field(fieldName="pu_location_id", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="pu_notes", fieldDetails="NTEXT", isPrimaryKey=False),
    Field(fieldName="del_location_id", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="del_notes", fieldDetails="NTEXT", isPrimaryKey=False),
    Field(fieldName="driver_name", fieldDetails="NVARCHAR(63)", isPrimaryKey=False),
    Field(fieldName="pod_signee", fieldDetails="NVARCHAR(255)", isPrimaryKey=False),
    Field(fieldName="pod_time_signed", fieldDetails="DATETIME2", isPrimaryKey=False),
    Field(fieldName="pod_notes", fieldDetails="NTEXT", isPrimaryKey=False),
    Field(fieldName="status_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="rating_weight_charges", fieldDetails="MONEY", isPrimaryKey=False),
    Field(fieldName="rating_fuel_charges", fieldDetails="MONEY", isPrimaryKey=False),
    Field(fieldName="rating_service_charges", fieldDetails="MONEY", isPrimaryKey=False),
    Field(fieldName="rating_total_charges", fieldDetails="MONEY", isPrimaryKey=False),
    Field(fieldName="rating_total_expenses", fieldDetails="MONEY", isPrimaryKey=False),
    Field(fieldName="rating_storage_charges", fieldDetails="MONEY", isPrimaryKey=False),
    Field(fieldName="rating_adjustments", fieldDetails="MONEY", isPrimaryKey=False),
    Field(fieldName="rating_notes", fieldDetails="NTEXT", isPrimaryKey=False),
    Field(fieldName="quickbooks_customer_list_id", fieldDetails="NVARCHAR(50)", isPrimaryKey=False),
    Field(fieldName="quickbooks_customer_name", fieldDetails="NVARCHAR(50)", isPrimaryKey=False),
    Field(fieldName="quickbooks_invoice_reference_number", fieldDetails="NVARCHAR(50)", isPrimaryKey=False),
    Field(fieldName="quickbooks_line_sequence_number", fieldDetails="NVARCHAR(50)", isPrimaryKey=False),
    Field(fieldName="is_auto_assessorials", fieldDetails="BIT", isPrimaryKey=False),
    Field(fieldName="is_weight_charge_calculated", fieldDetails="BIT", isPrimaryKey=False),
]

overnightMaintenanceHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="date_overnight_maintenance", fieldDetails="DATETIME2", isPrimaryKey=False),
    Field(fieldName="user_id", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="open_orders_in", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="open_order_assessorials_in", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="open_order_dimensions_in", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="open_order_drivers_in", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="open_order_attachments_in", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="invoiced_orders_in", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="invoiced_order_assessorials_in", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="invoiced_order_dimensions_in", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="invoiced_order_drivers_in", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="invoiced_order_attachments_in", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="remaining_orders_in", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="remaining_order_assessorials_in", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="remaining_order_dimensions_in", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="remaining_order_drivers_in", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="remaining_order_attachments_in", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="open_orders_out", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="open_order_assessorials_out", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="open_order_dimensions_out", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="open_order_drivers_out", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="open_order_attachments_out", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="invoiced_orders_out", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="invoiced_order_assessorials_out", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="invoiced_order_dimensions_out", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="invoiced_order_drivers_out", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="invoiced_order_attachments_out", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="remaining_orders_out", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="remaining_order_assessorials_out", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="remaining_order_dimensions_out", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="remaining_order_drivers_out", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="remaining_order_attachments_out", fieldDetails="INTEGER DEFAULT (0)", isPrimaryKey=False),
]

phoneFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="country_code", fieldDetails="NVARCHAR(3) NOT NULL", isPrimaryKey=False),
    Field(fieldName="area_code", fieldDetails="NVARCHAR(5) NOT NULL", isPrimaryKey=False),
    Field(fieldName="phone_number", fieldDetails="NVARCHAR(14) NOT NULL", isPrimaryKey=False),
    Field(fieldName="phone_extension", fieldDetails="NVARCHAR(4)", isPrimaryKey=False),
]

positionChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="position_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="user_id", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL", isPrimaryKey=False),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL", isPrimaryKey=False),
]

positionFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="position_name", fieldDetails="NVARCHAR(35) NOT NULL", isPrimaryKey=False),
    Field(fieldName="security_level", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL", isPrimaryKey=False),
    Field(fieldName="branch_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
]

postalCodeRegionFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="postal_code_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="region_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
]

postalCodeFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="postal_code", fieldDetails="NVARCHAR(15) NOT NULL", isPrimaryKey=False),
]

rateAreaFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="rate_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="area", fieldDetails="NVARCHAR(1) NOT NULL", isPrimaryKey=False),
    Field(fieldName="rate_min", fieldDetails="MONEY", isPrimaryKey=False),
    Field(fieldName="rate_100", fieldDetails="MONEY", isPrimaryKey=False),
    Field(fieldName="rate_1000", fieldDetails="MONEY", isPrimaryKey=False),
    Field(fieldName="rate_2000", fieldDetails="MONEY", isPrimaryKey=False),
    Field(fieldName="rate_5000", fieldDetails="MONEY", isPrimaryKey=False),
    Field(fieldName="rate_max", fieldDetails="MONEY", isPrimaryKey=False),
]

rateChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="rate_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="user_id", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL", isPrimaryKey=False),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL", isPrimaryKey=False),
]

rateFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="rate_name", fieldDetails="NVARCHAR(31) NOT NULL", isPrimaryKey=False),
    Field(fieldName="branch_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="is_default", fieldDetails="BIT NOT NULL DEFAULT (0)", isPrimaryKey=False),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL DEFAULT (1)", isPrimaryKey=False),
    Field(fieldName="date_added", fieldDetails="DATETIME2", isPrimaryKey=False),
    Field(fieldName="added_by_user_id", fieldDetails="INTEGER", isPrimaryKey=False),
]
    
regionFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="country_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="iso_code", fieldDetails="NVARCHAR(6) NOT NULL", isPrimaryKey=False),
    Field(fieldName="region_name", fieldDetails="NVARCHAR(63) NOT NULL", isPrimaryKey=False),
]

specialChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="special_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="user_id", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL", isPrimaryKey=False),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL", isPrimaryKey=False),
]

specialFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="old_id", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="branch_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="weekday", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="start_time", fieldDetails="TIME NOT NULL", isPrimaryKey=False),
    Field(fieldName="end_time", fieldDetails="TIME NOT NULL", isPrimaryKey=False),
    Field(fieldName="area", fieldDetails="NVARCHAR(1) NOT NULL", isPrimaryKey=False),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL DEFAULT (1)", isPrimaryKey=False),
]

userChangeHistoryFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="user_changed_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="user_id", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="date_changed", fieldDetails="DATETIME2 NOT NULL", isPrimaryKey=False),
    Field(fieldName="changes", fieldDetails="NTEXT NOT NULL", isPrimaryKey=False),
]

userFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER NOT NULL IDENTITY(1, 1)", isPrimaryKey=True),
    Field(fieldName="username", fieldDetails="NVARCHAR(63) UNIQUE NOT NULL", isPrimaryKey=False),
    Field(fieldName="email", fieldDetails="NVARCHAR(255) NOT NULL", isPrimaryKey=False),
    Field(fieldName="password_hash", fieldDetails="NVARCHAR(255)", isPrimaryKey=False),
    Field(fieldName="password_salt", fieldDetails="NVARCHAR(32)", isPrimaryKey=False),
    Field(fieldName="name_prefix", fieldDetails="NVARCHAR(6)", isPrimaryKey=False),
    Field(fieldName="first_name", fieldDetails="NVARCHAR(31)", isPrimaryKey=False),
    Field(fieldName="last_name", fieldDetails="NVARCHAR(31)", isPrimaryKey=False),
    Field(fieldName="name_suffix", fieldDetails="NVARCHAR(6)", isPrimaryKey=False),
    Field(fieldName="address_id", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="branch_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="commission_rate", fieldDetails="MONEY NOT NULL", isPrimaryKey=False),
    Field(fieldName="date_hired", fieldDetails="DATETIME2", isPrimaryKey=False),
    Field(fieldName="date_terminated", fieldDetails="DATETIME2", isPrimaryKey=False),
    Field(fieldName="phone_main_id", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="phone_home_id", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="phone_mobile_id", fieldDetails="INTEGER", isPrimaryKey=False),
    Field(fieldName="position_id", fieldDetails="INTEGER NOT NULL", isPrimaryKey=False),
    Field(fieldName="tsa_number", fieldDetails="NVARCHAR(12)", isPrimaryKey=False),
    Field(fieldName="tsa_type", fieldDetails="NVARCHAR(10)", isPrimaryKey=False),
    Field(fieldName="tsa_taken", fieldDetails="NVARCHAR(31)", isPrimaryKey=False),
    Field(fieldName="is_active", fieldDetails="BIT NOT NULL", isPrimaryKey=False),
    Field(fieldName="is_default_doc_owner", fieldDetails="BIT NOT NULL", isPrimaryKey=False),
    Field(fieldName="is_security_coordinator", fieldDetails="BIT NOT NULL", isPrimaryKey=False),
    Field(fieldName="is_tsa_trainer", fieldDetails="BIT NOT NULL", isPrimaryKey=False),
]
