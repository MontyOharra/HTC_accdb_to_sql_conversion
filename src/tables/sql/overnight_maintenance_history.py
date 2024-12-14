from ...imports import *

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

overnightMaintenanceHistoryIndexes: List[Index] = [
]

overnightMaintenanceHistoryForeignKeys: List[ForeignKey] = [
    ForeignKey('overnight_maintenance_history', 'user_id', 'user', 'id'),
]

def createOvernightMaintenanceHistoryTable(conn):
    overnightMaintenanceHistoryTable = SqlTable('overnight_maintenance_history', conn, overnightMaintenanceHistoryFields, overnightMaintenanceHistoryIndexes, overnightMaintenanceHistoryForeignKeys)
    overnightMaintenanceHistoryTable.createTable()
    overnightMaintenanceHistoryTable.addIndexes()

    return overnightMaintenanceHistoryTable

def addOvernightMaintenanceHistory(
    conn : Connection,
    dateOvernightMaintenance : str,
    userId : int,
    openOrdersIn : int,
    openOrderAssessorialsIn : int,
    openOrderDimensionsIn : int,
    openOrderDriversIn : int,
    openOrderAttachmentsIn : int,
    invoicedOrdersIn : int,
    invoicedOrderAssessorialsIn : int,
    invoicedOrderDimensionsIn : int,
    invoicedOrderDriversIn : int,
    invoicedOrderAttachmentsIn : int,
    remainingOrdersIn : int,
    remainingOrderAssessorialsIn : int,
    remainingOrderDimensionsIn : int,
    remainingOrderDriversIn : int,
    remainingOrderAttachmentsIn : int,
    openOrdersOut : int,
    openOrderAssessorialsOut : int,
    openOrderDimensionsOut : int,
    openOrderDriversOut : int,
    openOrderAttachmentsOut : int,
    invoicedOrdersOut : int,
    invoicedOrderAssessorialsOut : int,
    invoicedOrderDimensionsOut : int,
    invoicedOrderDriversOut : int,
    invoicedOrderAttachmentsOut : int,
    remainingOrdersOut : int,
    remainingOrderAssessorialsOut : int,
    remainingOrderDimensionsOut : int,
    remainingOrderDriversOut : int,
    remainingOrderAttachmentsOut : int,
) -> int:

    data = {
        'date_overnight_maintenance' : dateOvernightMaintenance,
        'user_id' : userId,
        'open_orders_in' : openOrdersIn,
        'open_order_assessorials_in' : openOrderAssessorialsIn,
        'open_order_dimensions_in' : openOrderDimensionsIn,
        'open_order_drivers_in' : openOrderDriversIn,
        'open_order_attachments_in' : openOrderAttachmentsIn,
        'invoiced_orders_in' : invoicedOrdersIn,
        'invoiced_order_assessorials_in' : invoicedOrderAssessorialsIn,
        'invoiced_order_dimensions_in' : invoicedOrderDimensionsIn,
        'invoiced_order_drivers_in' : invoicedOrderDriversIn,
        'invoiced_order_attachments_in' : invoicedOrderAttachmentsIn,
        'remaining_orders_in' : remainingOrdersIn,
        'remaining_order_assessorials_in' : remainingOrderAssessorialsIn,
        'remaining_order_dimensions_in' : remainingOrderDimensionsIn,
        'remaining_order_drivers_in' : remainingOrderDriversIn,
        'remaining_order_attachments_in' : remainingOrderAttachmentsIn,
        'open_orders_out' : openOrdersOut,
        'open_order_assessorials_out' : openOrderAssessorialsOut,
        'open_order_dimensions_out' : openOrderDimensionsOut,
        'open_order_drivers_out' : openOrderDriversOut,
        'open_order_attachments_out' : openOrderAttachmentsOut,
        'invoiced_orders_out' : invoicedOrdersOut,
        'invoiced_order_assessorials_out' : invoicedOrderAssessorialsOut,
        'invoiced_order_dimensions_out' : invoicedOrderDimensionsOut,
        'invoiced_order_drivers_out' : invoicedOrderDriversOut,
        'invoiced_order_attachments_out' : invoicedOrderAttachmentsOut,
        'remaining_orders_out' : remainingOrdersOut,
        'remaining_order_assessorials_out' : remainingOrderAssessorialsOut,
        'remaining_order_dimensions_out' : remainingOrderDimensionsOut,
        'remaining_order_drivers_out' : remainingOrderDriversOut,
        'remaining_order_attachments_out' : remainingOrderAttachmentsOut,
    }
    conn.sqlInsertRow('overnight_maintenance_history', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('overnight_maintenance_history')