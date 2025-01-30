from typing import Dict, Tuple, List
from pebble import ProcessPool
from concurrent.futures import as_completed
from rich.console import Console
from rich.progress import (
    Progress,
    MofNCompleteColumn,
    TextColumn
)
from .helpers import generateAccessDbNameCache
from .foreignKeyDefinitions import *
from .indexDefinitions import *
from .fieldDefinitions import *
from .rowConversionDefinitions import *

from src.classes.AccessConn import AccessConn

from src.types.types import Field, Index, ForeignKey
from collections.abc import Callable

def getMigrationDefinition(
    connFactories : Dict[str, Callable[[], AccessConn]], 
    tableName : str, 
    accessDbNameCache : Dict[str, str]
) -> Tuple[Tuple[List[Field], List[Index], List[ForeignKey]], Callable, str]:
    '''
        connFactories - Dictionary of connection factories for each database. The keys are the database names.
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
        rowConversionDefinition = getRowConversionFunction(conn, tableName)
        
        return (sqlTableDefinition, rowConversionDefinition, tableName)
    except KeyboardInterrupt:
        raise

def getMigrationDefinitions(
    conversionThreads : int,
    connFactories : Dict[str, Callable[[], AccessConn]], 
    tablesToMigrate : List[str]
) -> Tuple[
        Dict[str, Tuple[List[Field], List[Index], List[ForeignKey]]], 
        Dict[str, Callable[[], AccessConn]] 
      ]:
    '''
        conversionThreads - Number of threads to use for conversion.
        connFactories - Dictionary of connection factories for each database. The keys are the database names.
        tablesToMigrate - List of tables to migrate. If not provided, the default list, stored in conversionDefinitions/tablesToMigrate.py, will be used.
        
        Uses the getMigrationDefinition function to get the definition for each table via a multiprocessing pool.
        Returns a tuple containing the following:
            sqlTableDefinitions - Dictionary of table definitions for each table.
            accessConversionDefinitions - Dictionary of access conversion functions for each table. The keys are the table names.
    '''
    accessDbNameCache = generateAccessDbNameCache(tablesToMigrate)
    try:
        # Setup progress bar like "Getting migration definitions... [{completed} of {total}]"
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            MofNCompleteColumn(),
            transient=False
        ) as progressBar:
            taskId = progressBar.add_task(description="[yellow]Getting migration definitions...[/yellow]", total=len(tablesToMigrate))
            accessConversionDefinitions = {}
            sqlTableDefinitions = {}
            # Create a list of futures for each table
            # Loops through each table in tablesToMigrate
            # Schedules a function to get the SQL creation definition and access conversion definition for the table
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