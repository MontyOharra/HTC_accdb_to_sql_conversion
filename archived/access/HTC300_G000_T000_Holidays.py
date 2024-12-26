from ...imports import *

from ..sql.holiday import addHoliday

def convert_HTC300_G000_T000_Holidays(conn : Connection, row):
    addHoliday(
        conn,
        holidayName=row.HolidayName,
        holidayDate=row.HolidayDate
    )