CREATE TABLE [aci_data] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [city_id] INTEGER NOT NULL,
  [postal_code_id] INTEGER NOT NULL,
  [airport_code] NVARHCAR(5) NOT NULL,
  [carrier] NVARCHAR(50) DEFAULT '',
  [area] NVARCHAR(1) NOT NULL,
  [rate_min] MONEY,
  [rate_100] MONEY,
  [rate_1000] MONEY,
  [rate_2000] MONEY,
  [rate_5000] MONEY,
  [date_created] DATETIME2,
  [created_by] INTEGER,
  [branch_id] INTEGER NOT NULL,
  [is_active] BIT NOT NULL DEFAULT (1)
)
GO

CREATE TABLE [aci_data_change_history] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [aci_data_id] INTEGER NOT NULL,
  [user_id] INTEGER NOT NULL,
  [date_changed] DATETIME2 NOT NULL,
  [changes] NTEXT NOT NULL
)
GO

CREATE TABLE [address] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [address_line_1] NVARCHAR(127) NOT NULL,
  [address_line_2] NVARCHAR(63),
  [city_id] INTEGER NOT NULL,
  [postal_code_id] INTEGER NOT NULL
)
GO

CREATE TABLE [address_change_history] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [address_id] INTEGER NOT NULL,
  [user_id] INTEGER NOT NULL,
  [date_changed] DATETIME2 NOT NULL,
  [changes] NTEXT NOT NULL
)
GO

CREATE TABLE [agent] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [customer_id] INTEGER NOT NULL,
  [email_address] NVARCHAR(127) NOT NULL,
  [first_name] NVARCHAR(50),
  [last_name] NVARCHAR(50),
  [phone_id] INTEGER NOT NULL,
  [mobile_phone_id] INTEGER,
  [fax_id] INTEGER,
  [is_set_to_auto_notify_email] BIT NOT NULL DEFAULT (0),
  [is_active] BIT NOT NULL DEFAULT (1)
)
GO

CREATE TABLE [agent_change_history] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [agent_id] INTEGER NOT NULL,
  [user_id] INTEGER NOT NULL,
  [date_changed] DATETIME2 NOT NULL,
  [changes] NTEXT NOT NULL
)
GO

CREATE TABLE [agent_certification_test] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [agent_id] INTEGER NOT NULL,
  [certification_test_id] INTEGER NOT NULL,
  [date_tested] DATETIME2 NOT NULL,
  [test_score] INTEGER NOT NULL,
  [is_active] BIT NOT NULL DEFAULT (1)
)
GO

CREATE TABLE [archive_history] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [date_archived] DATETIME2,
  
  [open_orders] INTEGER DEFAULT (0),
  [open_order_assessorials] INTEGER DEFAULT (0),
  [open_order_dimensions] INTEGER DEFAULT (0),
  [open_order_drivers] INTEGER DEFAULT (0),
  [open_order_attachments] INTEGER DEFAULT (0),
  [invoiced_orders] INTEGER DEFAULT (0),
  [invoiced_order_assessorials] INTEGER DEFAULT (0),
  [invoiced_order_dimensions] INTEGER DEFAULT (0),
  [invoiced_order_drivers] INTEGER DEFAULT (0),
  [invoiced_order_attachments] INTEGER DEFAULT (0),
  [remaining_orders] INTEGER DEFAULT (0),
  [remaining_order_assessorials] INTEGER DEFAULT (0),
  [remaining_order_dimensions] INTEGER DEFAULT (0),
  [remaining_order_drivers] INTEGER DEFAULT (0),
  [remaining_order_attachments] INTEGER DEFAULT (0),
  [dock_orders] INTEGER DEFAULT (0),
  [dock_order_assessorials] INTEGER DEFAULT (0),
  [dock_order_dimensions] INTEGER DEFAULT (0),
  [dock_order_drivers] INTEGER DEFAULT (0),
  [dock_order_attachments] INTEGER DEFAULT (0),
  [service_orders] INTEGER DEFAULT (0),
  [service_order_assessorials] INTEGER DEFAULT (0),
  [service_order_dimensions] INTEGER DEFAULT (0),
  [service_order_drivers] INTEGER DEFAULT (0),
  [service_order_attachments] INTEGER DEFAULT (0),
  [active_order_history] INTEGER DEFAULT (0),
  [active_order_hawbs] INTEGER DEFAULT (0),
  [archived_orders] INTEGER DEFAULT (0),
  [archived_order_assessorials] INTEGER DEFAULT (0),
  [archived_order_dimensions] INTEGER DEFAULT (0),
  [archived_order_drivers] INTEGER DEFAULT (0),
  [archived_order_attachments] INTEGER DEFAULT (0),
  [archived_order_history] INTEGER DEFAULT (0),
  [archived_order_hawbs] INTEGER DEFAULT (0),
  [removed_orders] INTEGER DEFAULT (0),
  [removed_order_assessorials] INTEGER DEFAULT (0),
  [removed_order_dimensions] INTEGER DEFAULT (0),
  [removed_order_drivers] INTEGER DEFAULT (0),
  [removed_order_attachments] INTEGER DEFAULT (0),
  [removed_order_history] INTEGER DEFAULT (0),
  [removed_order_hawbs] INTEGER DEFAULT (0)
)
GO

CREATE TABLE [archive_error_log] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [order_id] INTEGER,
  [archive_date] DATETIME2,
  [user_id] INTEGER NOT NULL,
  [details] NTEXT
)
GO

CREATE TABLE [assessorial] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [branch_id] INTEGER NOT NULL,
  [old_id] INTEGER,
  [assessorial_name] NVARCHAR(31) NOT NULL,
  [min_charge] MONEY NOT NULL,
  [basis_type] nvarchar(255) NOT NULL CHECK ([basis_type] IN ('fixed', 'weight', 'prompt')) NOT NULL,
  [basis_portion] FLOAT NOT NULL,
  [basis_rate] MONEY,
  [user_prompt] NVARCHAR(127),
  [date_created] DATETIME2 NOT NULL,
  [notes] NTEXT,
  [is_active] BIT NOT NULL DEFAULT (1)
)
GO

CREATE TABLE [assessorial_change_history] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [assessorial_id] INTEGER NOT NULL,
  [user_id] INTEGER NOT NULL,
  [date_changed] DATETIME2 NOT NULL,
  [changes] NTEXT NOT NULL
)
GO

CREATE TABLE [branch] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [branch_name] NVARCHAR(63) NOT NULL,
  [company_id] INTEGER NOT NULL,
  [address_id] INTEGER NOT NULL,
  [airport_code] NVARCHAR(5) NOT NULL,
  [email] NVARCHAR(127) NOT NULL,
  [phone_id] INTEGER NOT NULL,
  [fax_id] INTEGER,
  [cartage_agent_type] NVARCHAR(15) NOT NULL DEFAULT 'cartage',
  [fuel_service_charge] MONEY NOT NULL,
  [transfer_rate] MONEY NOT NULL,
  [international_air_dim_divisor] INTEGER NOT NULL,
  [domestic_air_dim_divisor] INTEGER NOT NULL,
  [truck_dim_divisor] INTEGER NOT NULL,
  [aci_low] NVARCHAR(1) NOT NULL,
  [aci_high] NVARCHAR(1) NOT NULL,
  [notes] NTEXT,
  [is_active] BIT NOT NULL
)
GO

CREATE TABLE [branch_change_history] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [branch_id] INTEGER NOT NULL,
  [user_id] INTEGER NOT NULL,
  [date_changed] DATETIME2 NOT NULL,
  [changes] NTEXT NOT NULL
)
GO

CREATE TABLE [certification_test] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [certification_name] NVARCHAR(63) NOT NULL,
  [certification_test_trainer_id] INTEGER NOT NULL,
  [is_active] BIT NOT NULL
)
GO

CREATE TABLE [certification_test_change_history] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [certification_test_id] INTEGER NOT NULL,
  [user_id] INTEGER NOT NULL,
  [date_changed] DATETIME2 NOT NULL,
  [changes] NTEXT NOT NULL
)
GO

CREATE TABLE [certification_test_trainer] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [trainer_name] NVARCHAR(63),
  [is_active] BIT NOT NULL DEFAULT (1)
)
GO

CREATE TABLE [certification_test_trainer_change_history] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [certification_test_trainer_id] INTEGER NOT NULL,
  [user_id] INTEGER NOT NULL,
  [date_changed] DATETIME2 NOT NULL,
  [changes] NTEXT NOT NULL
)
GO

CREATE TABLE [city] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [city_name] NVARCHAR(63) NOT NULL
)
GO

CREATE TABLE [city_region] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [city_id] INTEGER NOT NULL,
  [region_id] INTEGER NOT NULL
)
GO

CREATE TABLE [city_postal_code] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [city_id] INTEGER NOT NULL,
  [postal_code_id] INTEGER NOT NULL,
  [lat] DECIMAL(9,2) NOT NULL,
  [lng] DECIMAL(9,2) NOT NULL
)
GO

CREATE TABLE [company] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [company_name] NVARCHAR(63) NOT NULL,
  [address_id] INTEGER NOT NULL,
  [phone_id] INTEGER NOT NULL,
  [airport_code] NVARCHAR(5),
  [fax_id] INTEGER,
  [cartage_agent_type] NVARCHAR(15) NOT NULL DEFAULT 'cartage',
  [employer_identification_no] NCHAR(10) UNIQUE NOT NULL,
  [email] NVARCHAR(255) UNIQUE NOT NULL,
  [scac] NVARCHAR(5) UNIQUE NOT NULL,
  [website] NVARCHAR(511),
  [notes] NTEXT,
  [logo_path] NVARCHAR(MAX),
  [is_tsa_compliant] BIT NOT NULL DEFAULT (0),
  [is_active] BIT NOT NULL DEFAULT (1)
)
GO

CREATE TABLE [company_change_history] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [company_id] INTEGER NOT NULL,
  [user_id] INTEGER NOT NULL,
  [date_changed] DATETIME2 NOT NULL,
  [changes] NTEXT NOT NULL
)
GO

CREATE TABLE [country] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [country_name] NVARCHAR(63) UNIQUE NOT NULL,
  [iso_code_2] NVARCHAR(2) UNIQUE NOT NULL,
  [iso_code_3] NVARCHAR(3) UNIQUE NOT NULL
)
GO

CREATE TABLE [customer] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [branch_id] INTEGER NOT NULL,
  [customer_name] NVARCHAR(63) NOT NULL,
  [address_id] INTEGER NOT NULL,
  [phone_id] INTEGER NOT NULL,
  [default_rate_id] INTEGER NOT NULL,
  [fuel_service_charge] MONEY NOT NULL,
  [qb_customer_ref_id] NVARCHAR(127),
  [qb_customer_ref_name] NVARCHAR(127),
  [is_qb_invoice_omitted] BIT NOT NULL,
  [is_active] BIT NOT NULL DEFAULT (1),
  [notes] NTEXT NOT NULL
)
GO

CREATE TABLE [customer_change_history] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [customer_id] INTEGER NOT NULL,
  [user_id] INTEGER NOT NULL,
  [date_changed] DATETIME2 NOT NULL,
  [changes] NTEXT NOT NULL
)
GO

CREATE TABLE [customer_default_assessorial] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [customer_id] INTEGER NOT NULL,
  [assessorial_id] INTEGER NOT NULL
)
GO

CREATE TABLE [fax] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [country_code] NVARCHAR(3) NOT NULL,
  [area_code] NVARCHAR(5) NOT NULL,
  [fax_number] NVARCHAR(14) NOT NULL,
  [fax_extension] NVARCHAR(4)
)
GO

CREATE TABLE [holiday] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [holiday_name] NVARCHAR(31) NOT NULL,
  [holiday_date] DATETIME2 NOT NULL
)
GO

CREATE TABLE [location] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [branch_id] INTEGER NOT NULL,
  [company_name] NVARCHAR(127),
  [location_name] NVARCHAR(127),
  [address_id] INTEGER NOT NULL,
  [aci_id] INTEGER NOT NULL,
  [contact_first_name] NVARCHAR(31),
  [contact_last_name] NVARCHAR(31),
  [contact_email] NVARCHAR(127),
  [contact_phone_id] INTEGER NOT NULL,
  [is_carrier] BIT NOT NULL DEFAULT (0),
  [is_local] BIT NOT NULL DEFAULT (0),
  [is_international] BIT NOT NULL DEFAULT (0),
  [default_wait_time] INTEGER,
  [is_active] BIT NOT NULL DEFAULT (1)
)
GO

CREATE TABLE [location_change_history] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [location_id] INTEGER NOT NULL,
  [user_id] INTEGER NOT NULL,
  [date_changed] DATETIME2 NOT NULL,
  [changes] NTEXT NOT NULL
)
GO

CREATE TABLE [location_default_assessorial] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [location_id] INTEGER NOT NULL,
  [assessorial_id] INTEGER NOT NULL
)
GO

CREATE TABLE [overnight_maintenance_history] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [date_overnight_maintenance] DATETIME2,
  [user_id] INTEGER DEFAULT (0),
  [open_orders_in] INTEGER DEFAULT (0),
  [open_order_assessorials_in] INTEGER DEFAULT (0),
  [open_order_dimensions_in] INTEGER DEFAULT (0),
  [open_order_drivers_in] INTEGER DEFAULT (0),
  [open_order_attachments_in] INTEGER DEFAULT (0),
  [invoiced_orders_in] INTEGER DEFAULT (0),
  [invoiced_order_assessorials_in] INTEGER DEFAULT (0),
  [invoiced_order_dimensions_in] INTEGER DEFAULT (0),
  [invoiced_order_drivers_in] INTEGER DEFAULT (0),
  [invoiced_order_attachments_in] INTEGER DEFAULT (0),
  [remaining_orders_in] INTEGER DEFAULT (0),
  [remaining_order_assessorials_in] INTEGER DEFAULT (0),
  [remaining_order_dimensions_in] INTEGER DEFAULT (0),
  [remaining_order_drivers_in] INTEGER DEFAULT (0),
  [remaining_order_attachments_in] INTEGER DEFAULT (0),
  [open_orders_out] INTEGER DEFAULT (0),
  [open_order_assessorials_out] INTEGER DEFAULT (0),
  [open_order_dimensions_out] INTEGER DEFAULT (0),
  [open_order_drivers_out] INTEGER DEFAULT (0),
  [open_order_attachments_out] INTEGER DEFAULT (0),
  [invoiced_orders_out] INTEGER DEFAULT (0),
  [invoiced_order_assessorials_out] INTEGER DEFAULT (0),
  [invoiced_order_dimensions_out] INTEGER DEFAULT (0),
  [invoiced_order_drivers_out] INTEGER DEFAULT (0),
  [invoiced_order_attachments_out] INTEGER DEFAULT (0),
  [remaining_orders_out] INTEGER DEFAULT (0),
  [remaining_order_assessorials_out] INTEGER DEFAULT (0),
  [remaining_order_dimensions_out] INTEGER DEFAULT (0),
  [remaining_order_drivers_out] INTEGER DEFAULT (0),
  [remaining_order_attachments_out] INTEGER DEFAULT (0)
)
GO

CREATE TABLE [order] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [branch_id] INTEGER NOT NULL,
  [order_type_id] INTEGER NOT NULL,
  [customer_id] INTEGER NOT NULL,
  [agent_id] INTEGER,
  [rate_id] INTEGER NOT NULL,
  [hawb] NVARCHAR(31),
  [mawb] NVARCHAR(31),
  [order_notes] NTEXT,
  [pu_time_start] DATETIME2 NOT NULL,
  [pu_time_end] DATETIME2 NOT NULL,
  [del_time_start] DATETIME2 NOT NULL,
  [del_time_end] DATETIME2 NOT NULL,
  [pu_location_id] INTEGER,
  [pu_contact_phone_id] INTEGER,
  [pu_contact_name] NVARCHAR(63),
  [pu_notes] NTEXT,
  [del_location_id] INTEGER,
  [del_contact_phone_id] INTEGER,
  [del_contact_name] NVARCHAR(63),
  [del_notes] NTEXT,
  [driver_name] NVARCHAR(63),
  [pod_signee] NVARCHAR(63),
  [pod_time_signed] DATETIME2,
  [pod_notes] NTEXT,
  [status_id] INTEGER NOT NULL,
  [rating_weight_charges] MONEY,
  [rating_fuel_charges] MONEY,
  [rating_service_charges] MONEY,
  [rating_total_charges] MONEY,
  [rating_total_expenses] MONEY,
  [rating_storage_charges] MONEY,
  [rating_adjustments] MONEY,
  [rating_notes] NTEXT,
  [quickbooks_customer_list_id] NVARCHAR(50),
  [quickbooks_customer_name] NVARCHAR(50),
  [quickbooks_invoice_reference_number] NVARCHAR(50),
  [quickbooks_line_sequence_number] NVARCHAR(50),
  [is_auto_assessorials] BIT,
  [is_weight_charge_calculated] BIT
)
GO

CREATE TABLE [order_change_history] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [order_id] INTEGER NOT NULL,
  [user_id] INTEGER NOT NULL,
  [date_changed] DATETIME2 NOT NULL,
  [changes] NTEXT NOT NULL
)
GO

CREATE TABLE [order_assessorial] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [order_id] INTEGER NOT NULL,
  [assessorial_id] INTEGER NOT NULL,
  [basis_count] DECIMAL(6,2),
  [total_charge] MONEY
)
GO

CREATE TABLE [order_attachment] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [order_id] INTEGER NOT NULL,
  [attachment_path] NVARCHAR(MAX),
  [file_size] DECIMAL(30,15)
)
GO

CREATE TABLE [order_dim] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [order_id] INTEGER NOT NULL,
  [unit_type] NVARCHAR(15),
  [unit_quantity] INTEGER,
  [unit_weight] INTEGER,
  [dim_height] INTEGER,
  [dim_width] INTEGER,
  [dim_length] INTEGER,
  [dim_weight] DECIMAL(20,10)
)
GO

CREATE TABLE [order_driver] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [order_id] INTEGER NOT NULL,
  [order_leg] NVARCHAR(1),
  [driver_role] NVARCHAR(1)
)
GO

CREATE TABLE [order_status] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [order_status_name] NVARCHAR(25) NOT NULL,
  [is_on_manifest] BIT NOT NULL,
  [is_set_to_auto_notify] BIT NOT NULL,
  [is_active] BIT NOT NULL,
  [branch_id] INTEGER NOT NULL
)
GO

CREATE TABLE [order_status_change_history] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [order_status_id] INTEGER NOT NULL,
  [user_id] INTEGER NOT NULL,
  [date_changed] DATETIME2 NOT NULL,
  [changes] NTEXT NOT NULL
)
GO

CREATE TABLE [order_type] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [order_type_name] NVARCHAR(31) NOT NULL
)
GO

CREATE TABLE [phone] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [country_code] NVARCHAR(3) NOT NULL,
  [area_code] NVARCHAR(5) NOT NULL,
  [phone_number] NVARCHAR(14) NOT NULL,
  [phone_extension] NVARCHAR(4)
)
GO

CREATE TABLE [position] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [position_name] NVARCHAR(35) NOT NULL,
  [security_level] INTEGER NOT NULL,
  [is_active] BIT NOT NULL,
  [branch_id] INTEGER NOT NULL
)
GO

CREATE TABLE [position_change_history] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [position_id] INTEGER NOT NULL,
  [user_id] INTEGER NOT NULL,
  [date_changed] DATETIME2 NOT NULL,
  [changes] NTEXT NOT NULL
)
GO

CREATE TABLE [postal_code] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [postal_code] NVARCHAR(15) NOT NULL
)
GO

CREATE TABLE [postal_code_region] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [postal_code_id] INTEGER NOT NULL,
  [region_id] INTEGER NOT NULL
)
GO

CREATE TABLE [rate] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [rate_name] NVARCHAR(31) NOT NULL,
  [branch_id] INTEGER NOT NULL,
  [is_default] BIT NOT NULL DEFAULT (0),
  [is_active] BIT NOT NULL DEFAULT (1),
  [date_added] DATETIME2,
  [added_by_user_id] INTEGER
)
GO

CREATE TABLE [rate_area] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [rate_id] INTEGER NOT NULL,
  [area] NVARCHAR(1) NOT NULL,
  [rate_min] MONEY,
  [rate_100] MONEY,
  [rate_1000] MONEY,
  [rate_2000] MONEY,
  [rate_5000] MONEY,
  [rate_max] MONEY
)
GO

CREATE TABLE [rate_change_history] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [rate_id] INTEGER NOT NULL,
  [user_id] INTEGER NOT NULL,
  [date_changed] DATETIME2 NOT NULL,
  [changes] NTEXT NOT NULL
)
GO

CREATE TABLE [region] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [country_id] INTEGER NOT NULL,
  [iso_code] CHAR NOT NULL,
  [region_name] NVARCHAR(63) NOT NULL
)
GO

CREATE TABLE [special] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [old_id] INTEGER,
  [branch_id] INTEGER NOT NULL,
  [weekday] INTEGER NOT NULL,
  [start_time] TIME NOT NULL,
  [end_time] TIME NOT NULL,
  [area] NVARCHAR(1) NOT NULL,
  [is_active] BIT NOT NULL DEFAULT (1)
)
GO

CREATE TABLE [special_change_history] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [special_id] INTEGER NOT NULL,
  [user_id] INTEGER NOT NULL,
  [date_changed] DATETIME2 NOT NULL,
  [changes] NTEXT NOT NULL
)
GO

CREATE TABLE [user] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [username] NVARCHAR(63) UNIQUE NOT NULL,
  [email] NVARCHAR(255) UNIQUE NOT NULL,
  [password_hash] NVARCHAR(255) NOT NULL,
  [password_salt] NVARCHAR(32) NOT NULL,
  [name_prefix] NVARCHAR(6),
  [first_name] NVARCHAR(31) NOT NULL,
  [last_name] NVARCHAR(31) NOT NULL,
  [name_suffix] NVARCHAR(6),
  [address_id] INTEGER NOT NULL,
  [branch_id] INTEGER NOT NULL,
  [commission_rate] MONEY NOT NULL,
  [date_hired] DATETIME2,
  [date_terminated] DATETIME2,
  [phone_main_id] INTEGER NOT NULL,
  [phone_home_id] INTEGER,
  [phone_mobile_id] INTEGER,
  [position_id] INTEGER NOT NULL,
  [tsa_number] NVARCHAR(10),
  [tsa_type] NVARCHAR(10),
  [tsa_taken] NVARCHAR(31),
  [is_active] BIT NOT NULL,
  [is_default_doc_owner] BIT NOT NULL,
  [is_security_coordinator] BIT NOT NULL,
  [is_tsa_trainer] BIT NOT NULL
)
GO

CREATE TABLE [user_change_history] (
  [id] INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [user_changed_id] INTEGER NOT NULL,
  [user_id] INTEGER NOT NULL,
  [date_changed] DATETIME2 NOT NULL,
  [changes] NTEXT NOT NULL
)
GO

CREATE INDEX [address_index_0] ON [address] ("city_id")
GO

EXEC sp_addextendedproperty
@name = N'Table_Description',
@value = 'This table is entirely new.
  Where noted, take addresses and populate this table with them.
',
@level0type = N'Schema', @level0name = 'dbo',
@level1type = N'Table',  @level1name = 'address';
GO

EXEC sp_addextendedproperty
@name = N'Column_Description',
@value = 'Function to convert phone numbers to IDs',
@level0type = N'Schema', @level0name = 'dbo',
@level1type = N'Table',  @level1name = 'agent',
@level2type = N'Column', @level2name = 'phone_id';
GO

EXEC sp_addextendedproperty
@name = N'Column_Description',
@value = 'Create function to turn address of branch into address row',
@level0type = N'Schema', @level0name = 'dbo',
@level1type = N'Table',  @level1name = 'branch',
@level2type = N'Column', @level2name = 'address_id';
GO

ALTER TABLE [aci_data] ADD FOREIGN KEY ([city_id]) REFERENCES [city] ([id])
GO

ALTER TABLE [aci_data] ADD FOREIGN KEY ([postal_code_id]) REFERENCES [postal_code] ([id])
GO

ALTER TABLE [aci_data] ADD FOREIGN KEY ([created_by]) REFERENCES [user] ([id])
GO

ALTER TABLE [aci_data] ADD FOREIGN KEY ([branch_id]) REFERENCES [branch] ([id])
GO

ALTER TABLE [aci_data_change_history] ADD FOREIGN KEY ([aci_data_id]) REFERENCES [aci_data] ([id])
GO

ALTER TABLE [aci_data_change_history] ADD FOREIGN KEY ([user_id]) REFERENCES [user] ([id])
GO

ALTER TABLE [address] ADD FOREIGN KEY ([city_id]) REFERENCES [city] ([id])
GO

ALTER TABLE [address] ADD FOREIGN KEY ([postal_code_id]) REFERENCES [postal_code] ([id])
GO

ALTER TABLE [address_change_history] ADD FOREIGN KEY ([address_id]) REFERENCES [address] ([id])
GO

ALTER TABLE [address_change_history] ADD FOREIGN KEY ([user_id]) REFERENCES [user] ([id])
GO

ALTER TABLE [agent] ADD FOREIGN KEY ([customer_id]) REFERENCES [customer] ([id])
GO

ALTER TABLE [agent] ADD FOREIGN KEY ([phone_id]) REFERENCES [phone] ([id])
GO

ALTER TABLE [agent] ADD FOREIGN KEY ([mobile_phone_id]) REFERENCES [phone] ([id])
GO

ALTER TABLE [agent] ADD FOREIGN KEY ([fax_id]) REFERENCES [fax] ([id])
GO

ALTER TABLE [agent_change_history] ADD FOREIGN KEY ([agent_id]) REFERENCES [agent] ([id])
GO

ALTER TABLE [agent_change_history] ADD FOREIGN KEY ([user_id]) REFERENCES [user] ([id])
GO

ALTER TABLE [agent_certification_test] ADD FOREIGN KEY ([agent_id]) REFERENCES [agent] ([id])
GO

ALTER TABLE [agent_certification_test] ADD FOREIGN KEY ([certification_test_id]) REFERENCES [certification_test] ([id])
GO

ALTER TABLE [archive_error_log] ADD FOREIGN KEY ([order_id]) REFERENCES [order] ([id])
GO

ALTER TABLE [archive_error_log] ADD FOREIGN KEY ([user_id]) REFERENCES [user] ([id])
GO

ALTER TABLE [assessorial] ADD FOREIGN KEY ([branch_id]) REFERENCES [branch] ([id])
GO

ALTER TABLE [assessorial_change_history] ADD FOREIGN KEY ([assessorial_id]) REFERENCES [assessorial] ([id])
GO

ALTER TABLE [assessorial_change_history] ADD FOREIGN KEY ([user_id]) REFERENCES [user] ([id])
GO

ALTER TABLE [branch] ADD FOREIGN KEY ([company_id]) REFERENCES [company] ([id])
GO

ALTER TABLE [branch] ADD FOREIGN KEY ([phone_id]) REFERENCES [phone] ([id])
GO

ALTER TABLE [branch] ADD FOREIGN KEY ([fax_id]) REFERENCES [fax] ([id])
GO

ALTER TABLE [branch_change_history] ADD FOREIGN KEY ([branch_id]) REFERENCES [branch] ([id])
GO

ALTER TABLE [branch_change_history] ADD FOREIGN KEY ([user_id]) REFERENCES [user] ([id])
GO

ALTER TABLE [certification_test] ADD FOREIGN KEY ([certification_test_trainer_id]) REFERENCES [certification_test_trainer] ([id])
GO

ALTER TABLE [certification_test_change_history] ADD FOREIGN KEY ([certification_test_id]) REFERENCES [certification_test] ([id])
GO

ALTER TABLE [certification_test_change_history] ADD FOREIGN KEY ([user_id]) REFERENCES [user] ([id])
GO

ALTER TABLE [certification_test_trainer_change_history] ADD FOREIGN KEY ([certification_test_trainer_id]) REFERENCES [certification_test_trainer] ([id])
GO

ALTER TABLE [certification_test_trainer_change_history] ADD FOREIGN KEY ([user_id]) REFERENCES [user] ([id])
GO

ALTER TABLE [city_region] ADD FOREIGN KEY ([city_id]) REFERENCES [city] ([id])
GO

ALTER TABLE [city_region] ADD FOREIGN KEY ([region_id]) REFERENCES [region] ([id])
GO

ALTER TABLE [city_postal_code] ADD FOREIGN KEY ([city_id]) REFERENCES [city] ([id])
GO

ALTER TABLE [city_postal_code] ADD FOREIGN KEY ([postal_code_id]) REFERENCES [postal_code] ([id])
GO

ALTER TABLE [company] ADD FOREIGN KEY ([address_id]) REFERENCES [address] ([id])
GO

ALTER TABLE [company] ADD FOREIGN KEY ([phone_id]) REFERENCES [phone] ([id])
GO

ALTER TABLE [company] ADD FOREIGN KEY ([fax_id]) REFERENCES [fax] ([id])
GO

ALTER TABLE [company_change_history] ADD FOREIGN KEY ([company_id]) REFERENCES [company] ([id])
GO

ALTER TABLE [company_change_history] ADD FOREIGN KEY ([user_id]) REFERENCES [user] ([id])
GO

ALTER TABLE [customer] ADD FOREIGN KEY ([branch_id]) REFERENCES [branch] ([id])
GO

ALTER TABLE [customer] ADD FOREIGN KEY ([address_id]) REFERENCES [address] ([id])
GO

ALTER TABLE [customer] ADD FOREIGN KEY ([phone_id]) REFERENCES [phone] ([id])
GO

ALTER TABLE [customer] ADD FOREIGN KEY ([default_rate_id]) REFERENCES [rate] ([id])
GO

ALTER TABLE [customer_change_history] ADD FOREIGN KEY ([customer_id]) REFERENCES [customer] ([id])
GO

ALTER TABLE [customer_change_history] ADD FOREIGN KEY ([user_id]) REFERENCES [user] ([id])
GO

ALTER TABLE [customer_default_assessorial] ADD FOREIGN KEY ([customer_id]) REFERENCES [customer] ([id])
GO

ALTER TABLE [customer_default_assessorial] ADD FOREIGN KEY ([assessorial_id]) REFERENCES [assessorial] ([id])
GO

ALTER TABLE [location] ADD FOREIGN KEY ([branch_id]) REFERENCES [branch] ([id])
GO

ALTER TABLE [location] ADD FOREIGN KEY ([address_id]) REFERENCES [address] ([id])
GO

ALTER TABLE [location] ADD FOREIGN KEY ([aci_id]) REFERENCES [aci_data] ([id])
GO

ALTER TABLE [location] ADD FOREIGN KEY ([contact_phone_id]) REFERENCES [phone] ([id])
GO

ALTER TABLE [location_change_history] ADD FOREIGN KEY ([location_id]) REFERENCES [location] ([id])
GO

ALTER TABLE [location_change_history] ADD FOREIGN KEY ([user_id]) REFERENCES [user] ([id])
GO

ALTER TABLE [location_default_assessorial] ADD FOREIGN KEY ([location_id]) REFERENCES [location] ([id])
GO

ALTER TABLE [location_default_assessorial] ADD FOREIGN KEY ([assessorial_id]) REFERENCES [assessorial] ([id])
GO

ALTER TABLE [overnight_maintenance_history] ADD FOREIGN KEY ([user_id]) REFERENCES [user] ([id])
GO

ALTER TABLE [order] ADD FOREIGN KEY ([branch_id]) REFERENCES [branch] ([id])
GO

ALTER TABLE [order] ADD FOREIGN KEY ([order_type_id]) REFERENCES [order_type] ([id])
GO

ALTER TABLE [order] ADD FOREIGN KEY ([customer_id]) REFERENCES [customer] ([id])
GO

ALTER TABLE [order] ADD FOREIGN KEY ([agent_id]) REFERENCES [agent] ([id])
GO

ALTER TABLE [order] ADD FOREIGN KEY ([rate_id]) REFERENCES [rate] ([id])
GO

ALTER TABLE [order] ADD FOREIGN KEY ([pu_location_id]) REFERENCES [location] ([id])
GO

ALTER TABLE [order] ADD FOREIGN KEY ([pu_contact_phone_id]) REFERENCES [phone] ([id])
GO

ALTER TABLE [order] ADD FOREIGN KEY ([del_location_id]) REFERENCES [location] ([id])
GO

ALTER TABLE [order] ADD FOREIGN KEY ([del_contact_phone_id]) REFERENCES [phone] ([id])
GO

ALTER TABLE [order] ADD FOREIGN KEY ([status_id]) REFERENCES [order_status] ([id])
GO

ALTER TABLE [order_change_history] ADD FOREIGN KEY ([order_id]) REFERENCES [order] ([id])
GO

ALTER TABLE [order_change_history] ADD FOREIGN KEY ([user_id]) REFERENCES [user] ([id])
GO

ALTER TABLE [order_assessorial] ADD FOREIGN KEY ([order_id]) REFERENCES [order] ([id])
GO

ALTER TABLE [order_assessorial] ADD FOREIGN KEY ([assessorial_id]) REFERENCES [assessorial] ([id])
GO

ALTER TABLE [order_attachment] ADD FOREIGN KEY ([order_id]) REFERENCES [order] ([id])
GO

ALTER TABLE [order_dim] ADD FOREIGN KEY ([order_id]) REFERENCES [order] ([id])
GO

ALTER TABLE [order_driver] ADD FOREIGN KEY ([order_id]) REFERENCES [order] ([id])
GO

ALTER TABLE [order_status] ADD FOREIGN KEY ([branch_id]) REFERENCES [branch] ([id])
GO

ALTER TABLE [order_status_change_history] ADD FOREIGN KEY ([order_status_id]) REFERENCES [order_status] ([id])
GO

ALTER TABLE [order_status_change_history] ADD FOREIGN KEY ([user_id]) REFERENCES [user] ([id])
GO

ALTER TABLE [position] ADD FOREIGN KEY ([branch_id]) REFERENCES [branch] ([id])
GO

ALTER TABLE [position_change_history] ADD FOREIGN KEY ([position_id]) REFERENCES [position] ([id])
GO

ALTER TABLE [position_change_history] ADD FOREIGN KEY ([user_id]) REFERENCES [user] ([id])
GO

ALTER TABLE [postal_code_region] ADD FOREIGN KEY ([postal_code_id]) REFERENCES [postal_code] ([id])
GO

ALTER TABLE [postal_code_region] ADD FOREIGN KEY ([region_id]) REFERENCES [region] ([id])
GO

ALTER TABLE [rate] ADD FOREIGN KEY ([branch_id]) REFERENCES [branch] ([id])
GO

ALTER TABLE [rate] ADD FOREIGN KEY ([added_by_user_id]) REFERENCES [user] ([id])
GO

ALTER TABLE [rate_area] ADD FOREIGN KEY ([rate_id]) REFERENCES [rate] ([id])
GO

ALTER TABLE [rate_change_history] ADD FOREIGN KEY ([rate_id]) REFERENCES [rate] ([id])
GO

ALTER TABLE [rate_change_history] ADD FOREIGN KEY ([user_id]) REFERENCES [user] ([id])
GO

ALTER TABLE [region] ADD FOREIGN KEY ([country_id]) REFERENCES [country] ([id])
GO

ALTER TABLE [special] ADD FOREIGN KEY ([branch_id]) REFERENCES [branch] ([id])
GO

ALTER TABLE [special_change_history] ADD FOREIGN KEY ([special_id]) REFERENCES [special] ([id])
GO

ALTER TABLE [special_change_history] ADD FOREIGN KEY ([user_id]) REFERENCES [user] ([id])
GO

ALTER TABLE [user] ADD FOREIGN KEY ([address_id]) REFERENCES [address] ([id])
GO

ALTER TABLE [user] ADD FOREIGN KEY ([branch_id]) REFERENCES [branch] ([id])
GO

ALTER TABLE [user] ADD FOREIGN KEY ([phone_main_id]) REFERENCES [phone] ([id])
GO

ALTER TABLE [user] ADD FOREIGN KEY ([phone_home_id]) REFERENCES [phone] ([id])
GO

ALTER TABLE [user] ADD FOREIGN KEY ([phone_mobile_id]) REFERENCES [phone] ([id])
GO

ALTER TABLE [user] ADD FOREIGN KEY ([position_id]) REFERENCES [position] ([id])
GO

ALTER TABLE [user_change_history] ADD FOREIGN KEY ([user_changed_id]) REFERENCES [user] ([id])
GO

ALTER TABLE [user_change_history] ADD FOREIGN KEY ([user_id]) REFERENCES [user] ([id])
GO
