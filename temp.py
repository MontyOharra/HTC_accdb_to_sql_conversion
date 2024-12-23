from .src.tables.new.fieldDefinitions import *
from .src.tables.new.indexDefinitions import *
from .src.tables.new.foreignKeyDefinitions import *
from .src.tables.new.conversionFunctions import *

            
sqlTableDefinitions = {
    'aci_data' :  (aciDataChangeHistoryFields, aciDataChangeHistoryIndexes, aciDataChangeHistoryForeignKeys)
    
}
    
accessTableConversions = {
    'HTC000 G010 T010 Company Info' : convert_HTC000_G010_T010_Company_Info
}

def generateNewTableLogDetails(tableNames):
    return {
        tableName : {
            'errorCount' : 0,
            'totalRows' : 0,
            'processedRows' : 0,
            'startTime' : None,
            'endTime' : None,
            'status' : None # Empty, Incomplete, Complete, Failure  
        }
        for tableName in tableNames
    }





from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Thread
from queue import Queue

from rich.console import Console
from rich.live import Live
from rich.table import Table
import time
import json

# Initialize the console
# Initialize the console
console = Console()

# Function to initialize the table
def createStatusTables(tableNames):
    sqlCreationStatusTable = Table(title="SQL Table Creation Status")
    sqlCreationStatusTable.add_column("Table Name", justify="left")
    sqlCreationStatusTable.add_column("Status", justify="center")

    accessConversionStatusTable = Table(title="Access Table Conversion Status")
    accessConversionStatusTable.add_column("Table Name", justify="left")
    accessConversionStatusTable.add_column("Status", justify="center")
    accessConversionStatusTable.add_column("Processed Rows", justify="right")
    accessConversionStatusTable.add_column("Total Rows", justify="right")
    accessConversionStatusTable.add_column("Errors", justify="right")

    # Initialize rows for both tables
    for tableName in tableNames['sql']:
        sqlCreationStatusTable.add_row(tableName, "")

    for tableName in tableNames['access']:
        accessConversionStatusTable.add_row(tableName, "", "0", "0", "0")

    return sqlCreationStatusTable, accessConversionStatusTable

# Function for the logging thread
def loggingThread(logQueue, tableNames, progressFile="progress.json"):
    sqlTable, accessTable = createStatusTables(tableNames)

    logDetails = {"sql": {}, "access": {}}  # Separate sections for progress tracking

    with Live(sqlTable, refresh_per_second=4, console=console) as liveSql, Live(accessTable, refresh_per_second=4, console=console) as liveAccess:
        while True:
            try:
                message = logQueue.get(timeout=1)  # Timeout to check periodically
                if message == "STOP":
                    break

                updateType, tableName, logData = message

                # Update SQL table creation status
                if updateType == "sql":
                    logDetails["sql"][tableName] = logData
                    for idx, row in enumerate(sqlTable.rows):
                        if row.cells[0].text == tableName:
                            sqlTable.rows[idx].cells[1].text = logData.get("status", "")
                            break
                    liveSql.update(sqlTable)

                # Update Access table conversion status
                elif updateType == "access":
                    logDetails["access"][tableName] = logData
                    for idx, row in enumerate(accessTable.rows):
                        if row.cells[0].text == tableName:
                            accessTable.rows[idx].cells[1].text = logData.get("status", "")
                            accessTable.rows[idx].cells[2].text = str(logData.get("processedRows", 0))
                            accessTable.rows[idx].cells[3].text = str(logData.get("totalRows", 0))
                            accessTable.rows[idx].cells[4].text = str(logData.get("errorCount", 0))
                            break
                    liveAccess.update(accessTable)

                # Save progress periodically
                with open(progressFile, 'w') as file:
                    json.dump(logDetails, file, indent=4)

            except Exception as e:
                console.print(f"[red]Logging thread encountered an error: {e}[/red]")
                break


def createSqlTable(connFactory, tableName, tableFields, tableIndexes):
    try:
        localConn : Connection = connFactory()
        localConn.sqlCreateTable(tableName, tableFields)
        for index in tableIndexes:
            localConn.sqlAddIndex(tableName, index.indexType, index.indexFields, index.indexName, index.isUnique)
    except Exception as err:
        sys.stdout.write(f'{err}\n')
    finally:
        localConn.close()
    
def addSqlForeignKey(connFactory, tableName, foreignKeys):
    try:
        localConn : Connection = connFactory()
        for foreignKey in foreignKeys:
            localConn.sqlAddForeignKey(tableName, foreignKey.fromTableField, foreignKey.toTableName, foreignKey.toTableField)
    except Exception as err:
        sys.stdout.write(f'{err}\n')
    finally:
        localConn.close()
    
def convertAccessTable(connFactory, tableName, rows, conversionFunction):
    try:
        tableLogDetails = logDetails[tableName]
        tableLogDetails['totalRows'] = len(rows)
        tableLogDetails['startTime'] = datetime.now()
        localConn : Connection = connFactory()
        if not rows:
            tableLogDetails['endTime'] = datetime.now()
            tableLogDetails['status'] = 'Empty'
            # Output to log
            return
            
        for row in rows:
            try:
                conversionFunction(localConn, row)
            except Exception as err:
                tableLogDetails['errorCount'] += 1
                logError(tableName, err)
                continue
            finally:
                tableLogDetails['processedRows'] += 1
                
        if tableLogDetails['processedRows'] != tableLogDetails['totalRows']:
            tableLogDetails['status'] = 'Incomplete'
        else:
            tableLogDetails['status'] = 'Complete'
            
        # Output to log
        updateLogFile(logDetails)
        updateTerminal(logDetails)
        
    except Exception as err:
        updateLogFile(logDetails)
        updateTerminal(logDetails)
    finally:
        localConn.close()

    
def createSqlTables(connFactory, maxThreads):
    with ThreadPoolExecutor(maxThreads) as executor:
        futures = [
            executor.submit(
                createSqlTable, 
                connFactory, 
                tableName,
                definitions[0],
                definitions[1]
            )
            for tableName, definitions in sqlTableDefinitions.items()
        ]

        for future in as_completed(futures):
            future.result()
            
def addSqlForeignKeys(connFactory, maxThreads):
    with ThreadPoolExecutor(maxThreads) as executor:
        futures = [
            executor.submit(
                addSqlForeignKey, 
                connFactory, 
                tableName,
                definitions[2]
            )
            for tableName, definitions in sqlTableDefinitions.items()
        ]

        for future in as_completed(futures):
            future.result()

def convertTables(connFactory, maxThreads):
    with ThreadPoolExecutor(maxThreads) as executor:
        futures = [
            executor.submit(
                tableDetails['conversionFunction'], 
                connFactory, 
                tableName,
                accessTableConversions[tableName]
            )
            for tableName, tableDetails in accessTableConversions.items()
        ]

        for future in as_completed(futures):
            future.result()