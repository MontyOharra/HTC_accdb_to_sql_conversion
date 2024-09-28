CREATE TABLE [aci_data] (
  [id] INTEGER UNIQUE PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [city_id] INTEGER NOT NULL,
  [postal_code_id] INTEGER NOT NULL,
  [airport_id] INTEGER NOT NULL,
  [carrier] NVARCHAR(50) DEFAULT '',
  [area] NVARCHAR(1) NOT NULL,
  [rate_id] INTEGER NOT NULL,
  [is_active] BIT NOT NULL DEFAULT (1)
)
GO

CREATE TABLE [aci_data_change_history] (
  [id] INTEGER UNIQUE PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [aci_data_id] INTEGER NOT NULL,
  [user_id] INTEGER NOT NULL,
  [date_changed] DATETIME2 NOT NULL,
  [changes] NTEXT NOT NULL
)
GO

CREATE TABLE [address] (
  [id] INTEGER UNIQUE PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [address_line_1] NVARCHAR NOT NULL,
  [address_line_2] NVARCHAR,
  [city_id] INTEGER NOT NULL,
  [postal_code_id] INTEGER NOT NULL,
  [region_id] INTEGER NOT NULL,
  [is_carrier] BIT NOT NULL DEFAULT (0),
  [is_local] BIT NOT NULL DEFAULT (0),
  [is_international] BIT NOT NULL DEFAULT (0)
)
GO

CREATE TABLE [address_change_history] (
  [id] INTEGER UNIQUE PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [address_id] INTEGER NOT NULL,
  [user_id] INTEGER NOT NULL,
  [date_changed] DATETIME2 NOT NULL,
  [changes] NTEXT NOT NULL
)
GO

CREATE TABLE [agent] (
  [id] INTEGER UNIQUE PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [customer_id] INTEGER NOT NULL,
  [email_address] NVARCHAR(127) NOT NULL,
  [first_name] NVARCHAR(50),
  [last_name] NVARCHAR(50),
  [phone_id] INTEGER NOT NULL,
  [phone_mobile_id] INTEGER,
  [fax_id] INTEGER,
  [send_auto_email] BIT NOT NULL DEFAULT (0),
  [is_active] BIT NOT NULL DEFAULT (1)
)
GO

CREATE TABLE [agent_change_history] (
  [id] INTEGER UNIQUE PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [agent_id] INTEGER NOT NULL,
  [user_id] INTEGER NOT NULL,
  [date_changed] DATETIME2 NOT NULL,
  [changes] NTEXT NOT NULL
)
GO

CREATE TABLE [airport] (
  [id] INTEGER UNIQUE PRIMARY KEY NOT NULL IDENTITY(1, 1)
)
GO

CREATE TABLE [archive_history] (
  [id] INTEGER UNIQUE PRIMARY KEY NOT NULL IDENTITY(1, 1),
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

CREATE TABLE [assessorial] (
  [id] INTEGER UNIQUE PRIMARY KEY NOT NULL IDENTITY(1, 1)
)
GO

CREATE TABLE [assessorial_change_history] (
  [id] INTEGER UNIQUE PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [assessorial_id] INTEGER NOT NULL,
  [user_id] INTEGER NOT NULL,
  [date_changed] DATETIME2 NOT NULL,
  [changes] NTEXT NOT NULL
)
GO

CREATE TABLE [branch] (
  [id] INTEGER UNIQUE PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [company_id] INTEGER NOT NULL,
  [branch_name] NVARCHAR NOT NULL,
  [address_id] INTEGER NOT NULL,
  [airport_id] INTEGER NOT NULL,
  [phone_id] INTEGER NOT NULL,
  [email] NVARHCAR NOT NULL,
  [dim_divisor_id] INTEGER NOT NULL,
  [fuel_service_charge] MONEY NOT NULL,
  [transfer_rate] MONEY NOT NULL,
  [aci_low] VARCHAR NOT NULL,
  [aci_high] VARCHAR NOT NULL,
  [notes] NTEXT,
  [is_active] BIT NOT NULL
)
GO

CREATE TABLE [branch_change_history] (
  [id] INTEGER UNIQUE PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [branch_id] INTEGER NOT NULL,
  [user_id] INTEGER NOT NULL,
  [date_changed] DATETIME2 NOT NULL,
  [changes] NTEXT NOT NULL
)
GO

CREATE TABLE [city] (
  [id] INTEGER UNIQUE PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [city_name] NVARCHAR NOT NULL,
  [lat] DECIMAL NOT NULL,
  [long] DECIMAL NOT NULL,
  [region_id] INTEGER NOT NULL
)
GO

CREATE TABLE [company] (
  [id] INTEGER UNIQUE PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [address_id] INTEGER NOT NULL,
  [airport_id] INTEGER NOT NULL,
  [cartage_agent_type] NVARCHAR NOT NULL DEFAULT 'cartage',
  [company_name] NVARCHAR NOT NULL,
  [employer_identification_no] NCHAR UNIQUE NOT NULL,
  [email] NVARCHAR UNIQUE NOT NULL,
  [phone_id] INTEGER NOT NULL,
  [fax_id] INTEGER,
  [is_active] BIT NOT NULL DEFAULT (1),
  [is_tsa_compliant] BIT NOT NULL DEFAULT (0),
  [notes] NTEXT,
  [scac] NVARCHAR UNIQUE NOT NULL,
  [website] NVARCHAR UNIQUE
)
GO

CREATE TABLE [company_change_history] (
  [id] INTEGER UNIQUE PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [company_id] INTEGER NOT NULL,
  [user_id] INTEGER NOT NULL,
  [date_changed] DATETIME2 NOT NULL,
  [changes] NTEXT NOT NULL
)
GO

CREATE TABLE [country] (
  [id] INTEGER UNIQUE PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [country_name] NVARCHAR UNIQUE NOT NULL,
  [iso_code] VARCHAR UNIQUE NOT NULL
)
GO

CREATE TABLE [customer] (
  [id] INTEGER UNIQUE PRIMARY KEY NOT NULL IDENTITY(1, 1)
)
GO

CREATE TABLE [customer_change_history] (
  [id] INTEGER UNIQUE PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [customer_id] INTEGER NOT NULL,
  [user_id] INTEGER NOT NULL,
  [date_changed] DATETIME2 NOT NULL,
  [changes] NTEXT NOT NULL
)
GO

CREATE TABLE [holiday] (
  [id] INTEGER UNIQUE PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [date] DATETIME NOT NULL,
  [holiday_name] VARCHAR(50) NOT NULL
)
GO

CREATE TABLE [dim_divisor] (
  [id] INTEGER UNIQUE PRIMARY KEY NOT NULL IDENTITY(1, 1)
)
GO

CREATE TABLE [fax] (
  [id] INTEGER UNIQUE PRIMARY KEY NOT NULL IDENTITY(1, 1)
)
GO

CREATE TABLE [order] (
  [order_number] INTEGER UNIQUE PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [customer_id] INTEGER NOT NULL,
  [hawb] VARCHAR,
  [mawb] VARCHAR,
  [notes] NTEXT,
  [order_type_id] INTEGER NOT NULL,
  [pu_date_end] DATETIME2 NOT NULL,
  [pu_date_start] DATETIME2 NOT NULL,
  [tarrif_id] INTEGER NOT NULL
)
GO

CREATE TABLE [overnight_maintenance_history] (
  [id] INTEGER UNIQUE PRIMARY KEY NOT NULL IDENTITY(1, 1)
)
GO

CREATE TABLE [order_status] (
  [id] INTEGER UNIQUE PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [is_active] BIT NOT NULL,
  [is_on_manifest] BIT NOT NULL,
  [is_set_to_auto_notify] BIT NOT NULL,
  [status_name] NVARCHAR UNIQUE NOT NULL
)
GO

CREATE TABLE [order_status_change_history] (
  [id] INTEGER UNIQUE PRIMARY KEY NOT NULL IDENTITY(1, 1)
)
GO

CREATE TABLE [phone] (
  [id] INTEGER UNIQUE PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [area_code] VARCHAR NOT NULL,
  [country_code] VARCHAR NOT NULL,
  [phone_extension] VARCHAR,
  [phone_number] VARCHAR NOT NULL
)
GO

CREATE TABLE [position] (
  [id] INTEGER UNIQUE PRIMARY KEY NOT NULL IDENTITY(1, 1)
)
GO

CREATE TABLE [rate] (
  [id] INTEGER UNIQUE PRIMARY KEY NOT NULL IDENTITY(1, 1)
)
GO

CREATE TABLE [rate_area] (
  [id] INTEGER UNIQUE PRIMARY KEY NOT NULL IDENTITY(1, 1)
)
GO

CREATE TABLE [rate_change_history] (
  [id] INTEGER UNIQUE PRIMARY KEY NOT NULL IDENTITY(1, 1)
)
GO

CREATE TABLE [postal_code] (
  [id] INTEGER UNIQUE PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [postal_code] VARCHAR NOT NULL,
  [region_id] INTEGER NOT NULL
)
GO

CREATE TABLE [region] (
  [id] INTEGER UNIQUE PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [country_id] INTEGER NOT NULL,
  [iso_code] CHAR NOT NULL,
  [region_name] NVARCHAR NOT NULL
)
GO

CREATE TABLE [user] (
  [id] INTEGER UNIQUE PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [address_id] INTEGER,
  [branch_id] INTEGER NOT NULL,
  [commission_rate] MONEY NOT NULL,
  [date_hired] DATETIME2,
  [date_terminated] DATETIME2,
  [email] NVARCHAR NOT NULL,
  [first_name] NVARCHAR NOT NULL,
  [is_active] BIT NOT NULL,
  [is_default_doc_owner] BIT NOT NULL,
  [is_security_coordinator] BIT NOT NULL,
  [is_tsa_trainer] BIT NOT NULL,
  [last_name] NVARCHAR NOT NULL,
  [name_prefix] NVARCHAR,
  [name_suffix] NVARCHAR,
  [password_hash] VARCHAR NOT NULL,
  [password_salt] NVARCHAR NOT NULL,
  [phone_home_id] INTEGER,
  [phone_main_id] INTEGER NOT NULL,
  [phone_mobile_id] INTEGER,
  [position_id] INTEGER,
  [tsa_number] VARCHAR,
  [tsa_type] VARCHAR,
  [username] NVARCHAR UNIQUE NOT NULL
)
GO

CREATE TABLE [user_change_history] (
  [id] INTEGER UNIQUE PRIMARY KEY NOT NULL IDENTITY(1, 1)
)
GO

EXEC sp_addextendedproperty
@name = N'Table_Description',
@value = 'FIELDS REMOVED:
  aci_key
  plus_one,
  rate_100,
  rate_1000,
  rate_2000,
  rate_5000,
  date_created

OVERALL NOTES:
  aci_data_change_history to store all the user creation and update fields

  aci_key fields removed in favor of id field. Other tables might reference this id,
    so make a function to get the id from the aci_key
',
@level0type = N'Schema', @level0name = 'dbo',
@level1type = N'Table',  @level1name = 'aci_data';
GO

EXEC sp_addextendedproperty
@name = N'Column_Description',
@value = 'Function to change city, state, and country combo into city_id',
@level0type = N'Schema', @level0name = 'dbo',
@level1type = N'Table',  @level1name = 'aci_data',
@level2type = N'Column', @level2name = 'city_id';
GO

EXEC sp_addextendedproperty
@name = N'Column_Description',
@value = 'Function to convert airport_code into airport_id',
@level0type = N'Schema', @level0name = 'dbo',
@level1type = N'Table',  @level1name = 'aci_data',
@level2type = N'Column', @level2name = 'postal_code_id';
GO

EXEC sp_addextendedproperty
@name = N'Column_Description',
@value = 'Maybe change into area_id?',
@level0type = N'Schema', @level0name = 'dbo',
@level1type = N'Table',  @level1name = 'aci_data',
@level2type = N'Column', @level2name = 'area';
GO

EXEC sp_addextendedproperty
@name = N'Column_Description',
@value = 'Function to convert fields rate_min through rate_5000 to a rate_id',
@level0type = N'Schema', @level0name = 'dbo',
@level1type = N'Table',  @level1name = 'aci_data',
@level2type = N'Column', @level2name = 'rate_id';
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

ALTER TABLE [aci_data] ADD FOREIGN KEY ([airport_id]) REFERENCES [airport] ([id])
GO

ALTER TABLE [aci_data_change_history] ADD FOREIGN KEY ([aci_data_id]) REFERENCES [aci_data] ([id])
GO

ALTER TABLE [aci_data_change_history] ADD FOREIGN KEY ([user_id]) REFERENCES [user] ([id])
GO

ALTER TABLE [address] ADD FOREIGN KEY ([city_id]) REFERENCES [city] ([id])
GO

ALTER TABLE [address] ADD FOREIGN KEY ([postal_code_id]) REFERENCES [postal_code] ([id])
GO

ALTER TABLE [address] ADD FOREIGN KEY ([region_id]) REFERENCES [region] ([id])
GO

ALTER TABLE [address_change_history] ADD FOREIGN KEY ([address_id]) REFERENCES [address] ([id])
GO

ALTER TABLE [address_change_history] ADD FOREIGN KEY ([user_id]) REFERENCES [user] ([id])
GO

ALTER TABLE [agent] ADD FOREIGN KEY ([customer_id]) REFERENCES [customer] ([id])
GO

ALTER TABLE [agent] ADD FOREIGN KEY ([phone_id]) REFERENCES [phone] ([id])
GO

ALTER TABLE [agent] ADD FOREIGN KEY ([phone_mobile_id]) REFERENCES [phone] ([id])
GO

ALTER TABLE [agent] ADD FOREIGN KEY ([fax_id]) REFERENCES [fax] ([id])
GO

ALTER TABLE [agent_change_history] ADD FOREIGN KEY ([agent_id]) REFERENCES [agent] ([id])
GO

ALTER TABLE [agent_change_history] ADD FOREIGN KEY ([user_id]) REFERENCES [user] ([id])
GO

ALTER TABLE [assessorial_change_history] ADD FOREIGN KEY ([assessorial_id]) REFERENCES [assessorial] ([id])
GO

ALTER TABLE [assessorial_change_history] ADD FOREIGN KEY ([user_id]) REFERENCES [user] ([id])
GO

ALTER TABLE [branch] ADD FOREIGN KEY ([company_id]) REFERENCES [company] ([id])
GO

ALTER TABLE [branch] ADD FOREIGN KEY ([airport_id]) REFERENCES [airport] ([id])
GO

ALTER TABLE [branch] ADD FOREIGN KEY ([phone_id]) REFERENCES [phone] ([id])
GO

ALTER TABLE [branch] ADD FOREIGN KEY ([dim_divisor_id]) REFERENCES [dim_divisor] ([id])
GO

ALTER TABLE [branch_change_history] ADD FOREIGN KEY ([branch_id]) REFERENCES [branch] ([id])
GO

ALTER TABLE [branch_change_history] ADD FOREIGN KEY ([user_id]) REFERENCES [user] ([id])
GO

ALTER TABLE [city] ADD FOREIGN KEY ([region_id]) REFERENCES [region] ([id])
GO

ALTER TABLE [company] ADD FOREIGN KEY ([address_id]) REFERENCES [address] ([id])
GO

ALTER TABLE [company] ADD FOREIGN KEY ([airport_id]) REFERENCES [airport] ([id])
GO

ALTER TABLE [company] ADD FOREIGN KEY ([phone_id]) REFERENCES [phone] ([id])
GO

ALTER TABLE [company] ADD FOREIGN KEY ([fax_id]) REFERENCES [phone] ([id])
GO

ALTER TABLE [company_change_history] ADD FOREIGN KEY ([company_id]) REFERENCES [company] ([id])
GO

ALTER TABLE [company_change_history] ADD FOREIGN KEY ([user_id]) REFERENCES [user] ([id])
GO

ALTER TABLE [customer_change_history] ADD FOREIGN KEY ([customer_id]) REFERENCES [customer] ([id])
GO

ALTER TABLE [customer_change_history] ADD FOREIGN KEY ([user_id]) REFERENCES [user] ([id])
GO
