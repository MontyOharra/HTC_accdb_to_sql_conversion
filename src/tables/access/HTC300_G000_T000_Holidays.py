from ...imports import *

from ..sql.holiday import addHoliday

def convert_HTC300_G000_T000_Holidays(conn : Connection):
    tableName = 'HTC300_G000_T000 Holidays'
    holidayInfo = conn.accessGetTableInfo('htc300', tableName)
    for i, row in enumerate(holidayInfo, start=1):
        sys.stdout.write(f"\rConverting [{tableName}] Table: Currently converting row ({i}/{len(holidayInfo)})\033[K")
        sys.stdout.flush()
        addHoliday(
            conn,
            holidayName=row.HolidayName,
            holidayDate=row.HolidayDate
        )
    sys.stdout.write(f"\rCompleted [{tableName}] Conversion.\033[K\n")
    sys.stdout.flush()