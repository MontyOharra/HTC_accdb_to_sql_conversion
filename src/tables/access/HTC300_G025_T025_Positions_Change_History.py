from ...imports import *

from ..sql.position_change_history import addPositionChangeHistory


def convert_HTC300_G025_T025_Positions_Change_History(conn : Connection, row):
    addPositionChangeHistory(
        conn,
        dateChanged=row.PosnHist_Date,
        positionId=row.PosnHist_ID,
        userId=getUserIdFromUsername(conn, row.PosnHist_ChgdBy), 
        changes=row.PosnHist_Changes.strip() if not row.PosnHist_Changes.strip() == '' else 'N/A'
    )