from typing import Dict, Any, List, Optional, Tuple
import pyodbc

from ..types.types import Field, ValidIndexType
from datetime import datetime
from decimal import Decimal

from rich.console import Console

import traceback

def connectToAccessDatabase(accessDbPath):
    try:
        accessConnStr = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            rf'DBQ={accessDbPath};'
        )
        
        accessConn = pyodbc.connect(accessConnStr)
        return accessConn
    except pyodbc.Error as e:
        print(f"Access Connection Error: {e}")
        raise

class AccessConn:
    """
        A class for interacting with SQL Server and Access databases.
        Errors are handled via the handle error function for more information.
        
        htcAllPath - Path to the HTC_Apps folder.
        accessDbName - Name of the Access database.
    """
    def __init__(self, htcAllPath : str, dbName : str):
        accessConnStr = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            rf'DBQ={htcAllPath}{dbName};'
        )
        try:            
            self.conn : pyodbc.Connection = pyodbc.connect(accessConnStr)
            self.cursor = self.conn.cursor()
            self.htcAllPath = htcAllPath
            self.dbName = dbName

        except Exception as err:
            console = Console()
            console.print(f"[red]Error creating MS Access connection: {accessConnStr}[/red]")
            raise err
        
    def __del__(self):
        self.conn.close()

    def __str__(self):
        connStr = (
                r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
                rf'DBQ={self.htcAllPath}{self.dbName};'
            )
        return f"Access connection with connection string:\n    {connStr}"
    
    def select(
        self, 
        tableName: str,
        selectDetails : List[str | Dict[str, str]] | str | None = None,
        whereDetails : Dict[str, any] | str | None = None
    ) -> List[Any]:
        """
            Select data from a table.
            
            tableName - Name of the table to select data from.
            selectDetails - List of columns to select. Can be a single string or a list of dictionaries, where each dictionary contains a column name and an alias.
            whereDetails - Can be a full where string, or dictionary of field names and values to filter by with equality.
        """
        # Create column selection string
        selectColumnsClause : str
        if type(selectDetails) == list: # Columns can be a single string, or a dictionary, with the key being the column name and value being its alias
            selectColumnsClause = ', '.join([column if type(column) == str else f"{list(column.keys())[0]} AS {list(column.values())[0]}" for column in selectDetails])
        elif type(selectDetails) == str: # If column is single string
            selectColumnsClause = selectDetails
        else: # Otherwise select all columns
            selectColumnsClause = '*'
        
        if type(whereDetails) == dict:  
            whereArgs = []
            for tableField, fieldValue in whereDetails.items():
                if fieldValue == None: # If value is None, check if NULL in SQL
                    whereArgs.append(f"[{tableField}] IS NULL")
                elif type(fieldValue) == str: # If string type, double up any single quotations within the string for escaping
                    fieldValue = fieldValue.replace("'", "''")
                    whereArgs.append(f"[{tableField}] LIKE '{fieldValue}'")
                elif type(fieldValue) == int or type(fieldValue) == float: # IF numeric type, do not include quotations
                    whereArgs.append(f"[{tableField}] = {fieldValue}")
                elif type(fieldValue) == bool: # If boolean type, convert to 1/0 instead of true/false
                    if fieldValue == True:
                        whereArgs.append(f"[{tableField}] = 1")
                    else:
                        whereArgs.append(f"[{tableField}] = 0")
                else: # In all unchecked cases, check equality with single quotations around value
                    whereArgs.append(f"[{tableField}] = '{fieldValue}'")
                whereClause = ' AND '.join(whereArgs)
            
        elif type(whereDetails) == str:
          whereClause = whereDetails
        else:
          whereClause = ''

        selectSql: str = f"SELECT {selectColumnsClause} FROM [{tableName}] {f'WHERE {whereClause}' if whereClause else ''}"
        try:
          self.cursor.execute(selectSql)
          return self.cursor.fetchall()
        
        except Exception as err:
          self.handleError(
            action='select',
            info={
              'sqlStatement' : selectSql,
              'tableName' : tableName,
              'selectColumns' : selectDetails,
              'whereDetails' : whereDetails
            }
          )
      
    def getTableStructure(self, tableName: str) -> Tuple[Dict[str, str], List[str]]:
        """
            tableName - Name of the table to retrieve structure from.
            
            Returns a tuple containing the following:
                columnsInfo - A dictionary of column names and their details.
                primaryKeyColumns - A list of primary key column names.
        """
        try:
            # Execute a dummy query to get metadata
            self.cursor.execute(f"SELECT TOP 1 * FROM [{tableName}]")
            # Fetch column metadata from cursor description
            columnDescriptions = self.cursor.description
            columnsInfo = {columnDescription[0] : self.getColumnDetails(columnDescription) for columnDescription in columnDescriptions}
            # Get primary key columns
            primaryKeyColumns = [row[8] for row in self.cursor.statistics(tableName) if row[5]=='PrimaryKey']

            return (columnsInfo, primaryKeyColumns) 

        except Exception as err:
            self.handleError(
                action='getTableStructure',
                info={
                    "tableName": tableName,
                    "sqlStatement": f"SELECT TOP 1 * FROM [{tableName}]"
                }
            )
                      
    def getColumnDetails(self, columnDescription : Tuple[any]) -> str:
        """
            columnDescription - A tuple containing information about the column.
            
            Get the column details from a column description.
            Edit within the if block to add or remove column details.
      
            Returns a string containing the column details.
        """
        typeCode : any = columnDescription[1]
        displaySize : int = columnDescription[2]
        internalSize : int = columnDescription[3]
        precision : int = columnDescription[4]
        scale : int = columnDescription[5]
        nullable : bool = columnDescription[6]
        columnDetails : str = ''
        if typeCode == bool:
            columnDetails += 'BIT'
        elif typeCode == int:
            columnDetails += 'INTEGER'
        elif typeCode == float or typeCode == Decimal:
            if scale == 0:
                columnDetails += 'INTEGER'
            else:
                columnDetails += f'DECIMAL({precision},{scale})'
        # Case strings to be NTEXT or NVARCHAR
        elif typeCode == str:
            if columnDescription[3] == 1073741823:
                columnDetails += 'NTEXT'
            else:
                columnDetails += 'NVARCHAR'
                columnDetails += f'({columnDescription[3]})'
        elif typeCode == datetime:
            columnDetails += 'DATETIME'
        else:
            columnDetails += 'UNKNOWN_TYPE'
            
        if not nullable:
            columnDetails += ' NOT NULL'
          
        return columnDetails

    def handleError(self, action : str, info: Optional[Dict[str, Any]] = None) -> None:
        """
            A function to handle errors in the SQL Server connection.
            
            action - Name of the action that caused the error.
            info - Optional dictionary of additional information about the error.
        """
        self.conn.rollback()
        
        errorMessage: str = '\n'
        if action == f"select":
          errorMessage += f'Error selecting data from [{info['tableName']}].\n    Details:\n'
          if (type(info['whereDetails']) == dict):  
            for fieldName, fieldValue in info['whereDetails'].items():
              errorMessage += f'        Name: [{fieldName}], Value: [{fieldValue}], Type: [{type(fieldValue)}]\n'
          elif (type(info['whereDetails']) == str):
            errorMessage += f'        Where Clause: [{info["whereDetails"]}]\n'
        elif action == 'getTableStructure':
          errorMessage += f'Error getting table structure from [{info['tableName']}] in [{self.dbName}].\n'
        else:
          errorMessage += "Error message not defined\n"
          
        # Create error message with SQL statement, error details, and detailed error message
        # Add indentation to custom errors.
        errorMessage += f'\n    SQL:\n        {info['sqlStatement']}'
        errorMessage += '\n    Detailed Error Message:'
        errorMessage += f'\n        {''.join([char if char != "\n" else '\n        ' for char in traceback.format_exc()])}'
        errorMessage += '\n'
        
        raise Exception(errorMessage)
