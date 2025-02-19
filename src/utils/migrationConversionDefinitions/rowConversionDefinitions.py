from .addDataFunctionDefinitions import *

from src.classes.AccessConn import AccessConn

from collections.abc import Callable
from functools import partial
from typing import Any

def getRowConversionFunction(
    accessConn : AccessConn, 
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
        columnNames = [field.fieldName for field in accessConn.getTableStructure(accessTableName)]
        if accessTableName == 'HTC000_G090_T010 Staff':
            return partial(migrateUserRow, columnNames=columnNames)
        return partial(migrateAccessRow, columnNames=columnNames, accessTableName=accessTableName)
    except Exception as err:
        raise err
  
    