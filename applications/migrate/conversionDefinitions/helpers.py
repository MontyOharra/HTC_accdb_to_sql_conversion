from typing import Dict, List

def generateAccessDbNameCache(
    tableNames : List[str]
) -> Dict[str, str]:
    '''
        tableNames - List of table names to generate the cache for.
        
        Returns a dictionary of table names and their cached database names.
        
        Used to speed up conversion process.
        The normal behavior is to cache the first 6 characters of the table name as the database name.
        If there are any tables that have a different naming convention, this function can be edited to add or remove cached database names.
        Edit this function to add or remove cached database names.
    '''
    accessDbNameCache = {
        tableName : tableName[0:6].lower() for tableName in tableNames
    }
    # Table names that have a different naming convention
    accessDbNameCache['HTC400_G900_T010 Archive Event Log'] = 'htc400archive'
    accessDbNameCache['HTC320_ThisCoBr'] = 'htc321'
    accessDbNameCache['HTC350D_G020_T020 NameSwap_ChgHistory'] = 'htc350d'
    return accessDbNameCache

def getNullReplacement(
    fieldType : str
) -> any:
    if fieldType in ('int', 'float', 'decimal'):
        return 0
    elif fieldType in ('nvarchar', 'varchar', 'ntext', 'text'):
        return ''