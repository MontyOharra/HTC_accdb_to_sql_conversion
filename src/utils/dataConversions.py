import re
from collections import defaultdict

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

def getPhoneAreaCode(phoneString):
    plainPhoneString = getPhonePlainNumber(phoneString)
    return plainPhoneString[0:3] if len(plainPhoneString) >= 10 else ''

def getPhoneNumber(phoneString):
    plainPhoneString = getPhonePlainNumber(phoneString)
    return plainPhoneString[3:10] if len(plainPhoneString) >= 10 else ''

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
