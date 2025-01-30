from .addDataFunctionDefinitions import *

from src.classes.AccessConn import AccessConn

from collections.abc import Callable
from functools import partial
from typing import Any

def getRowConversionFunction(
    conn : AccessConn, 
    accessTableName : str
) -> Callable[[Callable[[], SqlServerConn], list[Any]], None]:
    '''
        conn - Access connection object.
        accessTableName - Name of the table to get the conversion function for.
        
        Returns a partial function that converts the Access table to the SQL table.
        The conversion function is defined based on the 
        Partial function is needed for multiprocessing compatible use.
    '''
    try:
        columnNames = list(conn.getTableStructure(accessTableName)[0].keys())
        return partial(migrateAccessRow, columnNames=columnNames, accessTableName=accessTableName)
    except Exception as err:
        raise err
  
    