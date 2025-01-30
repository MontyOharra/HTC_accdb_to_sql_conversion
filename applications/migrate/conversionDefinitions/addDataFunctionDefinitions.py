from .helpers import getNullReplacement

from src.classes.SqlServerConn import SqlServerConn

from collections.abc import Callable
from typing import Any

def migrateAccessRow(
    columnNames : list[str],
    accessTableName : str,
    sqlConnFactory : Callable[[], SqlServerConn], 
    row : list[Any], 
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
            
    sqlConn.insertRow(accessTableName, data)