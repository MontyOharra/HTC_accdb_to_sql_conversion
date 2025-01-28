
from .conversionDefinitions.tablesToMigrate import tablesToMigrate as tablesToMigrateDefault
from typing import Dict
from src.types.types import Field
from src.utils.conversionHelpers import generateAccessDbNameCache, accessConversionFunction

from collections.abc import Callable

from pebble import ProcessPool
from concurrent.futures import as_completed
from rich.console import Console

def getHelper(connFactories, tableName, accessDbNameCache):
    try:
        console = Console()
        console.print("[yellow]Getting migration definitions...[/yellow]")
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

def getMigrationDefinitions(conversionThreads : int, connFactories : Dict[str, Callable], tablesToMigrate=tablesToMigrateDefault):
    accessDbNameCache = generateAccessDbNameCache(tablesToMigrate)
    try:
        accessConversionDefinitions = {}
        sqlTableDefinitions = {}
        with ProcessPool(max_workers=conversionThreads) as executor:
            futures = [
                executor.schedule(
                    getHelper, args=[
                        connFactories,
                        tableName,
                        accessDbNameCache
                    ]
                )
              for tableName in tablesToMigrate
            ]
            for future in as_completed(futures):
                try:
                    (sqlTableDefinition, accessConversionDefinition, tableName) = future.result()
                    sqlTableDefinitions[tableName] = sqlTableDefinition
                    accessConversionDefinitions[tableName] = accessConversionDefinition
                except KeyboardInterrupt:
                    for f in futures:
                        f.cancel()
                    raise
                    
        return (sqlTableDefinitions, accessConversionDefinitions)
    except KeyboardInterrupt:
        for f in futures:
            f.cancel()
        raise

def getSqlTableFields(conn, accessTableName):
    structureDetails = conn.getTableStructure(accessTableName)
    fields = []
    
    for column in structureDetails['columnsInfo']:
        fields.append(Field(column['name'], column['details'] + ' NOT NULL' if column['details'][-8:] != 'NOT NULL' else column['details']))
    
    return fields

def getSqlTableIndexes(connFactory, accessTableName):
    return []

def getSqlTableForeignKeys(connFactory, accessTableName):
    return []

def getAccessConversionFunction(conn, accessTableName):
    columnNames = [column['name'] for column in conn.getTableStructure(accessTableName)['columnsInfo']]
    from functools import partial
    return partial(accessConversionFunction, columnNames=columnNames, accessTableName=accessTableName)