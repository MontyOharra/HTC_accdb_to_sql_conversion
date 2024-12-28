from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich.live import Live

def createSqlCreationStatusesTable(sqlCreationTableStatuses):
    table = Table(title="SQL Creation Statuses")
    table.add_column("Table Name", justify="left")
    table.add_column("Creation Status", justify="center")
    table.add_column("Indexes Status", justify="center")
    table.add_column("Start Time", justify="center")
    table.add_column("End Time", justify="center")
    for tableName, statusDict in sqlCreationTableStatuses.items():
        creationStatus = statusDict.get("creationStatus", "Not Started")
        indexesStatus = statusDict.get("indexesStatus", "Not Started")
        startTime = statusDict.get("startTime", "")
        endTime = statusDict.get("endTime", "")
        table.add_row(tableName, creationStatus, indexesStatus, startTime, endTime)
    return table

def createAccessConversionStatusesTable(accessConversionTableStatuses):
    table = Table()
    table.add_column("Table Name", justify="left")
    table.add_column("Status", justify="center")
    table.add_column("Processed Rows", justify="right")
    table.add_column("Total Rows", justify="right")
    table.add_column("Errors", justify="right")
    table.add_column("Start Time", justify="center")
    table.add_column("End Time", justify="center")

    for tableName, details in accessConversionTableStatuses.items():
        status = details.get("status", "Not Started")
        processed = str(details.get("processedRows", 0))
        total = str(details.get("totalRows", 0))
        errors = str(details.get("errorCount", 0))

        startTime = str(details.get("startTime", ""))
        endTime = str(details.get("endTime", ""))

        table.add_row(
            tableName,
            status,
            processed,
            total,
            errors,
            startTime,
            endTime
        )
    return table

def createSqlForeignKeyStatusesTable(sqlForeignKeyTableStatuses):
    table = Table()
    table.add_column("Table Name", justify="left")
    table.add_column("Foreign Key Name", justify="left")
    table.add_column("Status", justify="center")
    for tableName, foreignKeyDict in sqlForeignKeyTableStatuses.items():
        for foreignKeyName, statusDict in foreignKeyDict.items():
            status = statusDict.get("status", "Not Started")
            table.add_row(tableName, foreignKeyName, status)
    return table


def outputLoggingTable(logQueue, tableType, tableData, successMessage):
    """
    Listens for messages like:
        ("sqlCreation", tableName, "status", "In Progress")
        ...
    Updates tablesData accordingly, rebuilds Rich tables, & calls live.update().
    """
    console = Console()
    with Live(console=console, refresh_per_second=1, transient=False, vertical_overflow='visible') as live:
        while True:
            try:
                message = logQueue.get(timeout=1)
            except KeyboardInterrupt:
                break
            except:
                # If no message for 1s, just re-check
                continue

            if message == "STOP":
                # Optionally write final progress
                '''try:
                    with open(progressFile, 'w') as pf:
                        json.dump(sqlCreationData, pf, indent=4)
                except Exception:
                    console.print("[red]Error writing progress file on STOP[/red]")'''
                break

            # Expecting 4-tuple
            if isinstance(message, tuple) and len(message) == 3:
                (tableName, detailName, newValue) = message
                if tableName in tableData.keys():
                    tableData[tableName][detailName] = newValue
                else:
                    console.print(f"[yellow]Unknown table: {tableName}[/yellow]")
            else:
                console.print(f"[red]Invalid message: {message}[/red]")

            # Rebuild the tables
            if tableType == "sqlCreate":
                tableSetupFunction = createSqlCreationStatusesTable
                panelTitle = "SQL Creation Statuses"
            elif tableType == "accessConvert":
                tableSetupFunction = createAccessConversionStatusesTable
                panelTitle = "Access Conversion Statuses"
            else:
                raise Exception(f"Invalid table type: {tableType}")
            table = tableSetupFunction(tableData)            
            live.update(table)

    console.print(f"[green]{successMessage}[/green]")