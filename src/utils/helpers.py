import os
import sys
import platform
from rich.console import Console
from rich.prompt import Prompt, Confirm

from typing import Dict, List

def isCompiled():
    return getattr(sys, 'frozen', False)

def getRootDir():
    currentFileDir = os.path.dirname(os.path.abspath(__file__))
    # Start at the current file's directory and move two levels up
    if isCompiled():
        return currentFileDir
    else:
        return os.path.abspath(os.path.join(currentFileDir, "../../"))

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