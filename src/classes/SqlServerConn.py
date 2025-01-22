from typing import Dict, Any, List, Optional, Tuple
import pyodbc

from ..types.types import Field, ValidIndexType
from datetime import datetime
from decimal import Decimal

from rich.console import Console

import traceback

class SqlServerConn:
    """
        A class for interacting with SQL Server and Access databases.
        Errors are handled via the handle error function for more information.
        
        sqlDriver - Driver for the SQL Server database
        sqlServerName - Name of the SQL Server database
        sqlDatabaseName - Name of the SQL Server database
    """
    def __init__(self, sqlDriver : str, sqlServerName : str, sqlDatabaseName : str):
        self.console = Console()
        try:
            sqlServerConnString = (
                f'DRIVER={sqlDriver};'
                f'SERVER={sqlServerName};'
                f'DATABASE={sqlDatabaseName};'
                'Trusted_Connection=yes;'
            )
            self.conn : pyodbc.Connection = pyodbc.connect(sqlServerConnString)
            self.cursor = self.conn.cursor()

        except Exception as err:
            self.console.print(f"[red]Error creating SQL Server connection[/red]")
            raise err
        
    def __del__(self):
        self.conn.close()

    def dropTable(self, tableName : str) -> None:
        """
            Drops table in SQL Server database if it exists.
            
            tableName - Name of the table to be dropped
        """
        dropSql: str = f"DROP TABLE IF EXISTS [{tableName}]"
        try:
            self.cursor.execute(dropSql)
            self.conn.commit()
        except Exception as err:
            self.handleError(
                action='dropTable',
                info={
                    'sqlStatement' : dropSql,
                    'tableName' : tableName
                }
            )

    def createTable(self, tableName: str, tableFields: List[Field], primaryKeys: List[str] = None) -> None:
        """
            Create a table in the database.
          
            tableName - The name of the table to create.
            tableFields - A list of Field objects representing the fields in the table. 
            primaryKeys - A list of field names that are the primary keys for the table.
        """
        
        # Example: [field1] field1Details, [field2] field2Details, ...
        tableFieldsString = ', '.join([f'[{field.fieldName}] {field.fieldDetails}' for field in tableFields])
        # Example: CREATE TABLE [tableName] ([field1] field1Details, [field2] field2Details, ..., PRIMARY KEY ([field1], [field2], ...))
        createSql: str = f"CREATE TABLE [{tableName}] ({tableFieldsString}{f", PRIMARY KEY ({', '.join(primaryKeys)})" if primaryKeys else ''})"
        try:
            self.dropTable(tableName)
            self.cursor.execute(createSql)
            self.conn.commit()
        except Exception as err:
            self.handleError(
                action='createTable',
                info={
                    'sqlStatement' : createSql,
                    'tableName' : tableName
                }
            )
            
        
    def addIndex(self, tableName : str, indexName: str, indexType: ValidIndexType, indexFields: str | List[str], isUnique: bool = False) -> None:
      """
          Add an index to a table.
          
          tableName - Name of the table to add the index to.
          indexType - Type of index to add. Valid types are 'clustered' and 'nonclustered'.
          indexFields - Fields to include in the index. Can be a single field name or a list of field names.
          indexName - Name of the index to add.
          isUnique - Whether the index is unique.
      """
      uniqueClause: str = " UNIQUE " if isUnique else " "
      if type(indexFields) == str:
        indexFieldClause = f'[indexFields]'
      elif type(indexFields) == List:
        indexFieldClause = ', '.join(f'[{indexField}]' for indexField in indexFields)
      addIndexSql: str = f"CREATE{uniqueClause}{indexType.upper()} INDEX [{indexName}] ON [{tableName}] ({indexFieldClause})"
      try:
        self.sqlCursor.execute(addIndexSql)
        self.conn.commit()
      except Exception as err:
        self.handleError(
          action='addIndex',
          info={
            'sqlStatement' : addIndexSql,
            'tableName' : tableName,
            'indexType': indexType, 
            'indexFields': indexFields, 
            'indexName': indexName, 
            'isUnique': isUnique
          }
        )

    def addForeignKey(self, fromTableName: str, fromTableField: str, toTableName: str, toTableField: str) -> None:
      """
          Add foreign key to a table.
          
          fromTableName - Name of the table to add the foreign key to.
          fromTableField - Name of the field in the table to add the foreign key to.
          toTableName - Name of the table to add the foreign key to.
          toTableField - Name of the field in the table to add the foreign key to.
      """
      addForeignKeySql: str = f"ALTER TABLE [{fromTableName}] ADD FOREIGN KEY ([{fromTableField}]) REFERENCES [{toTableName}] ([{toTableField}])"
      try:
        self.sqlCursor.execute(addForeignKeySql)
        self.conn.commit()
      except Exception as err:
        self.handleError(
          action='addForeignKey',
          info={
            'sqlStatement' : addForeignKeySql,
            'fromTableName': fromTableName, 
            'fromTableField': fromTableField,
            'toTableName': toTableName,
            'toTableField': toTableField
          }
        )
        
    def getColumnType(self, tableName : str, columnName : str) -> str:
        """
            Get the data type of a column in a table.
            
            tableName - Name of the table to get the column type from.
            columnName - Name of the column to get the data type of.
        """
        selectSql: str = f"SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{tableName}' AND COLUMN_NAME = '{columnName}'"
        try:
          self.cursor.execute(selectSql)
          rows = self.cursor.fetchall()
          return rows[0][0]
        except Exception as err:
          self.handleError(
            action='getColumnType',
            info={
              'sqlStatement' : selectSql,
              'tableName' : tableName,
              'columnName' : columnName
            }
          )

    def insertRow(self, tableName : str, fields: Dict[str, Any], insertId : int = None, allowNulls : bool = True) -> None:
        """
            Insert a row into a table.
            
            tableName - Name of the table to insert the row into.
            fields - Dictionary of field names and values to insert into the table.
            insertId - Optional ID to insert into the table. If not provided, the database will generate an ID.
            allowNulls - Whether to allow null values in the insert. Default is True.
        """
        fieldNames: List[str] = list(fields.keys())
        fieldValues: List[Any] = []
        if not insertId == None: # If insertId is provided, add it to the beginning of the field list
            fieldNames.insert(0, 'id')
            fieldValues.insert(0, insertId)
          
        for value in fields.values():
            if type(value) == str:
                value = value.strip()
                if value == "":
                    fieldValues.append("NULL" if allowNulls else "''")
                else:
                    fieldValues.append(f"'{value.replace("'", "''")}'")
            elif type(value) == int or type(value) == float:
                fieldValues.append(value)
            elif type(value) == bool:
                if value == True:
                    fieldValues.append('1')
                else:
                    fieldValues.append('0')
            elif value == None:
                fieldValues.append("NULL" if allowNulls else "''")
            else:
                fieldValues.append(f"'{value}'")
        fieldNamesString: str = ', '.join(f'[{name}]' for name in fieldNames)
        insertValuesString: str = ', '.join(f"{value}" for value in fieldValues)
          
        insertSql: str = f"INSERT INTO [{tableName}] ({fieldNamesString}) VALUES ({insertValuesString})"
        try:
          if not insertId == None:
            self.cursor.execute(f"SET IDENTITY_INSERT [{tableName}] ON")
          self.cursor.execute(insertSql)
          if not insertId == None:
            self.cursor.execute(f"SET IDENTITY_INSERT [{tableName}] OFF")
            
          self.commit()
        except Exception as err:
          self.handleError(
            info={
              'sqlStatement' : insertSql,
              'tableName' : tableName,
              'fields': fields,
            }
          )
        
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
        
        # Create where clause
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

        tableName = f'[{tableName}]' if len(tableName.split(' ')) == 1 else tableName # Handle cases where table name is a joined table
        selectSql: str = f"SELECT {selectColumnsClause} FROM {tableName} {f'WHERE {whereClause}' if whereClause else ''}"
        try:
            self.cursor.execute(selectSql)
            return self.cursor.fetchall()
        except Exception as err:
            self.handleError(
                action='getInfo',
                info={
                    'sqlStatement' : selectSql,
                    'tableName' : tableName,
                    'selectColumns' : selectDetails,
                    'whereDetails': whereDetails,
              }
          )
    
    def getLastIdCreated(self, tableName : str) -> int:
        """
            Get the last ID created in a table.
            
            tableName - Name of the table to get the last ID from.
        """
        selectSql = f"SELECT IDENT_CURRENT('{tableName}') AS current_id"
        try:
            self.sqlCursor.execute(selectSql)
            rows = self.sqlCursor.fetchall()
            return rows[0].current_id
        except Exception as err:
            self.handleError(
                action='getLastIdCreated',
                info={
                    'sqlStatement' : selectSql,
                    'tableName': tableName
                }
            )

    def handleError(self, action : str, info: Optional[Dict[str, Any]] = None) -> None:
        """
            A function to handle errors in the SQL Server connection.
            
            action - Name of the action that caused the error.
            info - Optional dictionary of additional information about the error.
        """
        self.conn.rollback()
        
        errorMessage: str = '\n'
        if action == 'dropTable':
            errorMessage += f'Error dropping table [{info['tableName']}].\n'
        elif action == 'createTable':
          errorMessage += f'Error creating table [{info['tableName']}].\n'
        elif action == "addIndex":
          errorMessage += f"Error adding index onto [{info['tableName']}].\n    Details:\n"
          errorMessage += f"        Column Name: [{info['indexField']}], Index Type: '{info['indexType']}', Is Unique: {info['isUnique']}"
        elif action == "addForeignKey":
          errorMessage += f"Error adding foreign key to [{info['fromTableName']}].\n    Details:\n"
          errorMessage += f'            From field: [{info['fromTableField']}], Target table: [{info['toTableName']}], Target table field: [{info['toTableField']}]'
        elif action == 'getColumnType':
          errorMessage += f'Error getting column type from table: [{info['tableName']}], column: [{info['columnName']}].\n'
        elif action == 'insertRow':
          errorMessage += f'Error inserting row into [{info['tableName']}].\n    Details:\n'
          for fieldName, fieldValue in info['fields'].items():
            errorMessage += f'        Name: [{fieldName}], Value: [{fieldValue}], Type: [{type(fieldValue)}]\n'
        elif action == f"select":
          errorMessage += f'Error selecting data from [{info['tableName']}].\n    Details:\n'
          if (type(info['whereDetails']) == dict):  
            for fieldName, fieldValue in info['whereDetails'].items():
              errorMessage += f'        Name: [{fieldName}], Value: [{fieldValue}], Type: [{type(fieldValue)}]\n'
          elif (type(info['whereDetails']) == str):
            errorMessage += f'        Where Clause: [{info["whereDetails"]}]\n'
        elif action == 'getLastIdCreated':
          errorMessage += f'Error getting last id created in [{info['tableName']}].\n'
        else:
          errorMessage += "Error message not defined\n"
          
        # Create error message with SQL statement, error details, and detailed error message
        # Add indentation to custom errors.
        errorMessage += f'\n    SQL:\n        {info['sqlStatement']}'
        errorMessage += '\n    Detailed Error Message:'
        errorMessage += f'\n        {''.join([char if char != "\n" else '\n        ' for char in traceback.format_exc()])}'
        errorMessage += '\n'
        
        raise Exception(errorMessage)
