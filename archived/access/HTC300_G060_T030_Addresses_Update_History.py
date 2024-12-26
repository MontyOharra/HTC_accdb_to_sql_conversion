from ...imports import *

from ..sql.location_change_history import addLocationChangeHistory

def convert_HTC300_G060_T030_Addresses_Update_History(conn : Connection, row):
    addLocationChangeHistory(
        conn,
        locationId=row.Addr_ID,
        userId=getUserIdFromUsername(conn, row.Addr_UpdtLID),
        dateChanged=row.Addr_UpdtDate,
        changes=row.Addr_Chgs.strip() if not row.Addr_Chgs.strip() == '' else 'N/A'
    )