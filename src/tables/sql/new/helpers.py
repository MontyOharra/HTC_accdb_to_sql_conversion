from isocodes import subdivisions_countries, countries

from ....imports import Connection

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
      

def getUserIdFromUsername(conn : Connection, username) -> int:
    if username == None:
        return None
    if username.strip() == "":
        return None
      
    username = username.strip()
    
    userRow = conn.sqlGetInfo('user', 'id', f"[username] = '{username}'")
    if not userRow:
        return None
    
    return userRow[0].id