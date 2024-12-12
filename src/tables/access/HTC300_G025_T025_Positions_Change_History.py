from ...imports import *

from ..sql.position_change_history import addPositionChangeHistory


def convert_HTC300_G025_T025_Positions_Change_History(conn : Connection, row):
    addPositionChangeHistory(
        conn,
        dateChanged=row.STAT_UpdtDate,
        orderStatusId=row.STAT_Seq,
        userId=getUserIdFromUsername(conn, row.STAT_UpdtLID), 
        changes=row.STAT_Changes if not row.STAT_Changes.strip() == '' else 'N/A'
    )