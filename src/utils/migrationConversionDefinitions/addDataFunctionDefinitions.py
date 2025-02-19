from .helpers import getNullReplacement

from src.classes.SqlServerConn import SqlServerConn
from src.utils.helpers import generatePasswordHash, generatePasswordSalt

from collections.abc import Callable
from typing import Any

def migrateAccessRow(
    sqlConnFactory : Callable[[], SqlServerConn], 
    row : list[Any], 
    columnNames : list[str],
    accessTableName : str,
) -> None: 
    '''
        sqlConnFactory - A function that returns a SQL Server connection.
        row - A row from the Access table to convert.
        columnNames - A list of column names for the Access table.
        accessTableName - Name of the Access table.
        
        Defines a process for converting a row from the Access table to the SQL table.
    '''
    sqlConn = sqlConnFactory()
    data = {columnNames[i] : row[i] for i in range(len(columnNames))}
    
    for columnName, columnValue in data.items():
        # If the column is null replace it with the null replacement value
        # defined in the helpers file
        if columnValue == None:
            rowType = sqlConn.getColumnType(accessTableName, columnName)
            data[columnName] = getNullReplacement(rowType) 
            
    sqlConn.insertRow(accessTableName, data, setNulls=False)
    
def migrateUserRow(
    sqlConnFactory : Callable[[], SqlServerConn], 
    row : list[Any], 
    columnNames : list[str]
) -> None:
    sqlConn = sqlConnFactory()
    data = {columnNames[i] : row[i] for i in range(len(columnNames))}
    
    for columnName, columnValue in data.items():
        # If the column is null replace it with the null replacement value
        # defined in the helpers file
        if columnValue == None:
            rowType = sqlConn.getColumnType('HTC000_G090_T010 Staff', columnName)
            data[columnName] = getNullReplacement(rowType) 
            
    sqlConn.insertRow('HTC000_G090_T010 Staff', data, setNulls=False, isPasswordColumn=True)