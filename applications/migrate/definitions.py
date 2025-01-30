from typing import Dict, Tuple, List
from collections.abc import Callable
from functools import partial
from pebble import ProcessPool
from concurrent.futures import as_completed
from rich.console import Console
from rich.progress import (
    Progress,
    MofNCompleteColumn,
    TextColumn
)
from src.classes.AccessConn import AccessConn
from src.types.types import Field, Index, ForeignKey
from src.utils.conversionHelpers import generateAccessDbNameCache, accessConversionFunction
from .conversionDefinitions.tablesToMigrate import tablesToMigrate as tablesToMigrateDefault

def getMigrationDefinition(
    connFactories : Dict[str, Callable], 
    tableName : str, 
    accessDbNameCache : Dict[str, str]
) -> Tuple[Tuple[List[Field], List[Index], List[ForeignKey]], Callable, str]:
    '''
        connFactories - Dictionary of connection factories for each database.
        tableName - Name of the table to get the definition for.
        accessDbNameCache - Dictionary of cached database names for each table.
        
        Returns a tuple containing the following:
            sqlTableDefinition - A tuple containing the fields, indexes, and foreign keys for the table.
            accessConversionDefinition - A function that converts the Access table to the SQL table.
            tableName - The name of the table.
    '''
    try:
        connFactory = connFactories[accessDbNameCache[tableName]]
        conn = connFactory()
        sqlTableDefinition = (
            getSqlTableFields(conn, tableName), 
            getSqlTableIndexes(conn, tableName), 
            getSqlTableForeignKeys(conn, tableName)
        )
        accessConversionDefinition = getAccessConversionFunction(conn, tableName)
        
        return (sqlTableDefinition, accessConversionDefinition, tableName)
    except KeyboardInterrupt:
        raise

def getMigrationDefinitions(
    conversionThreads : int,
    connFactories : Dict[str, Callable], 
    tablesToMigrate : List[str] = tablesToMigrateDefault
) -> Tuple[Dict[str, Tuple[List[Field], List[Index], List[ForeignKey]]], Dict[str, Callable]]:
    '''
        conversionThreads - Number of threads to use for conversion.
        connFactories - Dictionary of connection factories for each database.
        tablesToMigrate - List of tables to migrate. If not provided, the default list, stored in conversionDefinitions/tablesToMigrate.py, will be used.
        
        Uses the getMigrationDefinition function to get the definition for each table via a multiprocessing pool.
        Returns a tuple containing the following:
            sqlTableDefinitions - Dictionary of table definitions for each table.
            accessConversionDefinitions - Dictionary of access conversion functions for each table.
    '''
    accessDbNameCache = generateAccessDbNameCache(tablesToMigrate)
    console = Console()
    console.print("[yellow]Getting migration definitions...[/yellow]")
    try:
        # Setup progress bar like "Getting migration definitions... [{completed} of {total}]"
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            MofNCompleteColumn(),
            transient=False
        ) as progressBar:
            taskId = progressBar.add_task(description="Getting migration definitions...", total=len(tablesToMigrate))
            accessConversionDefinitions = {}
            sqlTableDefinitions = {}
            with ProcessPool(max_workers=conversionThreads) as executor:
                futures = [
                    executor.schedule(
                        getMigrationDefinition, args=[
                            connFactories,
                            tableName,
                            accessDbNameCache
                        ]
                    )
                  for tableName in tablesToMigrate
                ]
                for future in as_completed(futures):
                    try:
                        # As futures complete, advance the progress bar
                        (sqlTableDefinition, accessConversionDefinition, tableName) = future.result()
                        progressBar.advance(taskId)
                        sqlTableDefinitions[tableName] = sqlTableDefinition
                        accessConversionDefinitions[tableName] = accessConversionDefinition
                    except Exception as err:
                        # Cancel all futures if an error occurs and raise exception
                        for f in futures:
                            f.cancel()
                        raise
                        
            return (sqlTableDefinitions, accessConversionDefinitions)
    except KeyboardInterrupt:
        for f in futures:
            f.cancel()
        raise

def getSqlTableFields(
    conn : AccessConn, 
    accessTableName : str
) -> List[Field]:
    '''
        conn - Access connection object.
        accessTableName - Name of the table to get the fields for.
        
        Returns a list of Field objects representing the fields in the table.
        Forces all fields to be NOT NULL
    '''
    structureDetails = conn.getTableStructure(accessTableName)
    fields = []
    
    for column in structureDetails['columnsInfo']:
        fields.append(Field(column['name'], column['details'] + ' NOT NULL' if column['details'][-8:] != 'NOT NULL' else column['details']))
    
    return fields

def getSqlTableIndexes(
    conn : AccessConn, 
    accessTableName : str
) -> List[Index]:
    '''
        conn - Access connection object.
        accessTableName - Name of the table to get the indexes for.
        
        Returns a list of Index objects representing the indexes in the table.
        
        TODO: Implement this
    '''
    return []

def getSqlTableForeignKeys(
    conn : AccessConn, 
    accessTableName : str
) -> List[ForeignKey]:
    '''
        conn - Access connection object.
        accessTableName - Name of the table to get the foreign keys for. 
        
        Returns a list of ForeignKey objects representing the foreign keys in the table.
        
        TODO: Implement this
    '''
    return []

def getAccessConversionFunction(
    conn : AccessConn, 
    accessTableName : str
) -> Callable:
    '''
        conn - Access connection object.
        accessTableName - Name of the table to get the conversion function for.
        
        Returns a function that converts the Access table to the SQL table.
    '''
    columnNames = [column['name'] for column in conn.getTableStructure(accessTableName)['columnsInfo']]
    return partial(accessConversionFunction, columnNames=columnNames, accessTableName=accessTableName)