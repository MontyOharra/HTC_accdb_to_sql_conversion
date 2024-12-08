from ...imports import *

from ..sql.holiday import addHoliday

def convert_HTC300_G000_T000_Holidays(conn : Connection):
    holidayInfo = conn.accessGetTableInfo('htc300', 'HTC300_G000_T000 Holidays')
    for row in holidayInfo:
        addHoliday(
            conn,
            holidayName=row.HolidayName,
            holidayDate=row.HolidayDate
        )
    print('Completed [HTC300_G000_T000 Holidays] Conversion.')