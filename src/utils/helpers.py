from typing import Dict, List
import os
import sys
import platform

def isCompiled():
    return getattr(sys, 'frozen', False)

def getRootDir():
    # Start at the current file's directory and move two levels up
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_file_dir, "../../"))
    return root_dir

def getLogDir():
    if isCompiled():
        if platform.system() == "Windows":
            return os.path.join(os.getenv("LOCALAPPDATA"), "YourAppName", "logs")
        else:
            return os.path.join(os.path.expanduser("~"), ".local", "share", "YourAppName", "logs")
    else:
        # Use the root directory to construct the log directory path
        return os.path.join(getRootDir(), "logs")


def chunkDictionary(dictionary : Dict[any, any], maxChunkSize : int) -> List[Dict[any, any]]:
    """
    Splits dictionary into a list of dictionaries,
    each containing at most maxChunkSize key/value pairs, in the
    original insertion order.
    """
    items = list(dictionary.items())
    return [dict(items[i:i+maxChunkSize]) for i in range(0, len(items), maxChunkSize)]