import re

from isocodes import subdivisions_countries, countries
from collections import defaultdict

from src.classes.SqlServerConn import SqlServerConn


def regionGet(**kwargs: str):
    try:
        key: str = next(iter(kwargs))
        return [
            element
            for element in subdivisions_countries.data
            if key in element and kwargs[key].lower() == element[key].lower()
        ]
    except IndexError:
        return {}
      
def countryGet(**kwargs: str):
    try:
        key: str = next(iter(kwargs))
        res = [
            element
            for element in countries.data
            if key in element and kwargs[key].lower() == element[key].lower()
        ]
        return res
        
    except IndexError:
        return {}

def getUserIdFromUsername(conn : SqlServerConn, username) -> int:
    if username == None:
        return None
    if username.strip() == "":
        return None
      
    username = username.strip()
    
    userRow = conn.sqlGetInfo('user', 'id', f"[username] = '{username}'")
    if not userRow:
        return None
    
    return userRow[0].id
  
def getCityLng(
    cityName: str,
    postalCode : str
) -> float:
    return 1

def getCityLat(
    cityName: str,
    postalCode : str
) -> float :
    return 1

def getPhonePlainNumber(phoneString):
    if phoneString == None:
        return ''
    
    numbers = ""
    for char in phoneString:
        if char.isdigit():
            numbers += char
    return numbers
  
def isPhoneNumber(phoneString):
    return getPhonePlainNumber(phoneString) != ''
from datetime import datetime

def fixDate(date):
    if not date:
      return None
    
    # Define potential formats for date and time
    date_formats = [
        "%Y-%m-%d",    # YYYY-MM-DD
        "%m/%d/%Y",    # MM/DD/YYYY
        "%d-%m-%Y",    # DD-MM-YYYY
        "%d/%m/%Y",    # DD/MM/YYYY
        "%m/%d/%y",    # MM/DD/YY, adjusted to 20YY if year < 2000
        "%m/%d/%Y",    # MM/D/YYYY
        "%m/%d/%y",    # MM/D/YY
        "%m/%d/%Y",    # M/D/YYYY
        "%m/%d/%y",    # M/D/YY
        "%m/%d/%Y",    # M/DD/YYYY
        "%m/%d/%y",    # M/DD/YY
        "%m-%d-%y",    # MM-DD-YY
    ]

    # Parse the date
    if isinstance(date, str):
        date = date.strip()
        try:
            if len(date.split('-')[2]) == 3:
            # Attempt to parse the three-digit year as an integer
                year = int(date.split('-')[2])
                if year == 202:
                    date = date.replace("202", "2022", 1)
                elif year == 203 or year == 223:
                    date = date.replace(str(year), "2023", 1)
        except:
            pass  # If parsing fails, let the normal format validation handle it
          
        try:
            if len(date.split('/')[2]) == 3:
            # Attempt to parse the three-digit year as an integer
                year = int(date.split('/')[2])
                if year == 202:
                    date = date.replace("202", "2022", 1)
                elif year == 203 or year == 223:
                    date = date.replace(str(year), "2023", 1)
                elif year == 209 or str(year) == "019":  
                    date = date.replace(str(year), "2019", 1)
            elif len(date.split('/')[2]) == 5:
                if str(year) == "02018":
                    date = date.replace("02018", "2018", 1)
            elif len(date.split('/')[1]) == 6:
                    date = date.replace(str(year), f"{str(year)[0:1]}/{str(year)[2:5]}", 1) 
        except:
            pass  # If parsing fails, let the normal format validation handle it
          
        for fmt in date_formats:
            try:
                parsed_date = datetime.strptime(date, fmt)
                # Adjust for formats like MM/DD/YY to enforce 20YY
                if fmt.endswith("%y") and parsed_date.year < 2000:
                    parsed_date = parsed_date.replace(year=parsed_date.year + 2000)
                date = parsed_date
                break
            except ValueError:
                continue
        else:
            print(f"[DEBUG] Error: Date format not recognized: {date}")
            return None
    
    return date
    
def fixTime(time):
    if not time:
        return None
      
    time_formats = [
        "%H:%M:%S.%f",  # HH:MM:SS.milliseconds
        "%H:%M:%S",     # HH:MM:SS
        "%H:%M",        # HH:MM
        "%I:%M %p",     # HH:MM AM/PM
        "%I:%M:%S %p",  # HH:MM:SS AM/PM
    ]
      
    if isinstance(time, str):
        if not time:
            return None
        for fmt in time_formats:
            try:
                time = datetime.strptime(time, fmt)
                break
            except ValueError:
                continue
        else:
            # Default to "00:00:00" if no valid time format is recognized
            timeString = "00:00:00"
            time = datetime.strptime(timeString, "%H:%M:%S")
            
    return time

def combineDateTime(date, time):
    date = fixDate(date)
    time = fixTime(time)
    
    if not date or not time:
        return None
      
    # Combine the date and time
    combined_datetime = datetime.combine(date.date(), time.time())
    # Format the output as "YYYY-MM-DD HH:MM:SS.{milliseconds}"
    return combined_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")

def getPhoneAreaCode(phoneString):
    plainPhoneString = getPhonePlainNumber(phoneString)
    return plainPhoneString[0:3] if len(plainPhoneString) >= 10 else ''

def getPhoneNumber(phoneString):
    plainPhoneString = getPhonePlainNumber(phoneString)
    return plainPhoneString[3:10] if len(plainPhoneString) >= 10 else ''

def infer_regex_patterns(strings):
    # Map for storing regex patterns and corresponding strings
    pattern_groups = defaultdict(list)

    for s in strings:
        # Generate regex pattern for the string
        pattern = re.sub(r'[0-9]', '0', s)  # Replace digits with '0'
        pattern = re.sub(r'[A-Za-z]', 'A', pattern)  # Replace letters with 'A'

        # Add string to the corresponding regex group
        pattern_groups[pattern].append(s)

    # Sort the strings in each group for better readability
    for pattern in pattern_groups:
        pattern_groups[pattern].sort()

    return pattern_groups

def correctPostalCode(postalCode):
    if postalCode == None:
        return ''
    
    usPostalCode4ErrorPattern = r'\d{4}'
    usPostalCode5Pattern = r'\d{5}'
    usPostalCode9Pattern = r'^\d{5}-\d{4}$'
    canadianPostalCodePattern = r'^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$'
    canadianPostalCodeNoSpacePattern = r'^[A-Za-z]\d[A-Za-z]\d[A-Za-z]\d$'
    
    postalCode = postalCode.strip()
    
    if postalCode == '300004':
        return '30004'
    elif postalCode == '6L9T5E5':
        return 'L9T 5E5'
    elif postalCode == 'NOJ1Y0':
        return 'N0J 1Y0'
    elif postalCode == 'M9W5LI':
        return 'M9W 5L1'
    elif postalCode == 'NYG4G8':
        return 'N4G 4G8'
    elif postalCode == '7515':
        return '75115'
    elif postalCode == '76050-':
        return '76050'
    elif re.fullmatch(canadianPostalCodeNoSpacePattern, postalCode):
        return postalCode[0:3] + ' ' + postalCode[3:]
    elif re.fullmatch(usPostalCode4ErrorPattern, postalCode):
        return '0' + postalCode
    elif re.fullmatch(usPostalCode5Pattern, postalCode) or re.fullmatch(usPostalCode9Pattern, postalCode) or re.fullmatch(canadianPostalCodePattern, postalCode):
        return postalCode
    else:
        return ''

def getAssessorialIds(assessorialIdString):
    if assessorialIdString == None:
        return []
      
    ids = []  
    for index, character in enumerate(assessorialIdString):
        if character.lower() == 'x':
            ids.append(index + 1)
            
    return ids

def generatePasswordSalt(saltLength : int) -> str:
    return ''.join([randomThing for randomThing in range(saltLength)])


def generatePasswordHash(password : str, passwordSalt : str) -> str:
    return password