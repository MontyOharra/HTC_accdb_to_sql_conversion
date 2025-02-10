import os
import sys
import platform

from typing import Any

def isCompiled():
    '''
        Returns True if the application is compiled, False otherwise.
    '''
    return getattr(sys, 'frozen', False)

def getRootDir():
    '''
        Returns the root directory of the application.
        If the application is compiled, returns the directory of the compiled file.
        Otherwise, returns the directory of the current file two levels up.
    '''
    # Start at the current file's directory and move two levels up
    if isCompiled():
        return os.path.dirname(sys.executable)
    else:
        currentFileDir = os.path.dirname(os.path.abspath(__file__))
        return os.path.abspath(os.path.join(currentFileDir, "../../"))

def getLogDir():
    '''
        Returns the log directory for the application.
        If the application is compiled, it uses the LOCALAPPDATA environment variable to determine the log directory.
        Otherwise, it uses the root directory of the application.
        On first run, if the log directory does not exist, it will be created.
    '''
    if isCompiled():
        if platform.system() == "Windows":
            appDataDir = os.getenv("LOCALAPPDATA")
            if appDataDir is None:
                err = ("LOCALAPPDATA environment variable not found. "
                       "Please set it to the directory where your application's data files are stored.")
                raise Exception(err)
            log_dir = os.path.join(appDataDir, "HTC_Conversion", "logs")
        else:
            log_dir = os.path.join(os.path.expanduser("~"), ".local", "share", "HTC_Conversion", "logs")
    else:
        log_dir = os.path.join(getRootDir(), "logs")
    
    # Create the directory if it does not exist.
    if not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir, exist_ok=True)
        except Exception as e:
            raise Exception(f"Could not create log directory at '{log_dir}': {e}")
    
    return log_dir
      

def chunkDictionary(dictionary : dict[Any, Any], maxChunkSize : int) -> list[dict[Any, Any]]:
    """
    Splits dictionary into a list of dictionaries,
    each containing at most maxChunkSize key/value pairs, in the
    original insertion order.
    """
    items = list(dictionary.items())
    return [dict(items[i:i+maxChunkSize]) for i in range(0, len(items), maxChunkSize)]
  
  
def generateAccessDbNameCache(
    tableNames : list[str]
) -> dict[str, str]:
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
