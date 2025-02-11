from threading import Thread
from queue import Queue, Empty
from typing import Dict
import os
import traceback

from rich.console import Console
from rich.text import Text
from rich.progress import (
    Progress,
    BarColumn,
    MofNCompleteColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
    ProgressColumn
)

from src.types.types import SqlCreationDetails, AccessConversionDetails, status
    
class StepStatusColumn(ProgressColumn):
    """
        A custom column to show the status of a given step:
        ("Not Started", "In Progress", "Completed").
    """

    def __init__(self, step_name: str):
        super().__init__()
        self.step_name = step_name

    def render(self, task) -> Text:
        # Get the step status from the task fields
        step_status : status = task.fields.get(self.step_name, "Not Started")

        if step_status == "Not Started":
            style = "dim"
        elif step_status == "In Progress":
            style = "yellow"
        elif step_status == "Complete":
            style = "green"
        else:
            style = "red"

        return Text(step_status, style=style)    

class ErrorCountColumn(ProgressColumn):
    """
        A column that displays how many errors have occurred for a task.
    """
    
    def __init__(self, step_name: str):
        super().__init__()
        self.step_name = step_name
        
    def render(self, task) -> Text:
        errors = task.fields.get(self.step_name, 0)
        style = "green" if errors == 0 else "red"
        return Text(f"Errors: {errors}", style=style)
      
def logErrors(errorLogQueue : Queue):
    console = Console()
    while True:
        try:
            message = errorLogQueue.get(timeout=.1)
        except Empty:
            continue
          
        if message == "STOP":
            break
          
        # Write error to error.log file within the same directory as the script
        # Error of the type (process, tableName, errorMessage)
        # Expecting 4-tuple
        if isinstance(message, tuple) and len(message) == 2:        
            process, exception = message
            errorsDir = f"C:/Users/Owner/Software_Projects/HTC_accdb_to_sql_conversion/errors/"
            if process == "sqlTableCreation":
                with open(f"{errorsDir}sqlTableCreation.log", "a") as errorLogFile:
                    errorLogFile.write(f"Error: {exception}\n")
            elif process == "accessTableConversion":
                with open(f"{errorsDir}accessTableConversion.log", "a") as errorLogFile:
                    errorLogFile.write(f"Error: {exception}\n")
        else:
            console.print(f"[red]Invalid message: {message}[/red]")

        
def logSqlCreationProgress(
    logQueue : Queue,
    tableCreationData : Dict[str, SqlCreationDetails]
):
    """
        Listens for messages sent in from a Queue object.
        Returns true if the process is complete., false otherwise.
        
        logQueue - Queue object to listen for messages from.
        tableData - Dictionary of table names and their status.
        successMessage - Message to display when the process is complete.
    """
    console = Console()
    console.print("[yellow]Creating SQL tables...[/yellow]")
    with Progress(
            "[progress.description]{task.description}",
            StepStatusColumn("creationStatus"),
            TextColumn("•"),
            StepStatusColumn("indexesStatus"),
            refresh_per_second=10,
            transient=False
    ) as progressBar:
        progressIds = {}
        for tableName, sqlCreationDetails in tableCreationData.items():
            progressIds[tableName] = progressBar.add_task(
                tableName,
                creationStatus=sqlCreationDetails.creationStatus,
                indexesStatus=sqlCreationDetails.indexesStatus
            )
        while True:
            try:
                message = logQueue.get(timeout=.1)
            except Empty:
                continue

            if message == "STOP":
                progressBar.stop()
                break
              
            # Expecting 3-tuple
            if isinstance(message, tuple) and len(message) == 2:
                (action, data) = message
                if action == "SET":
                    (tableName) = data
                    progressBar.update(progressIds[tableName], creationStatus="In Progress", indexesStatus="In Progress")
                elif action == "UPDATE":
                    (tableName, sqlCreationDetails) = data
                    if tableName in tableCreationData.keys():
                        progressBar.update(progressIds[tableName], 
                                           creationStatus=sqlCreationDetails.creationStatus, 
                                           indexesStatus=sqlCreationDetails.indexesStatus
                                          )
                    else:
                        console.print(f"[yellow]Unknown table: {tableName}[/yellow]")
                elif action == "ERROR":
                    progressBar.stop()
                    console.print(f"[red]{data}[/red]")
                    break   
                elif action == "SUCCESS":
                    progressBar.stop()
                    console.print(f"[green]{data}[/green]")
                    break
                else:
                    progressBar.stop()
                    console.print(f"[red]Invalid action: {action}[/red]")
                    break
            else:
                progressBar.stop()
                console.print(f"[red]Invalid message: {message}[/red]")
                break   
        
def logAccessConversionProgress(
    logQueue : Queue,
    tableConversionData : Dict[str, AccessConversionDetails]
) -> bool:
    """
        Listens for messages sent in from a Queue object.
        Returns true if the process is complete., false otherwise.
        
        logQueue - Queue object to listen for messages from.
        tableData - Dictionary of table names and their status.
        successMessage - Message to display when the process is complete.
    """
    console = Console()
    console.print("[yellow]Starting conversion...[/yellow]")
    with Progress(
        "[progress.description]{task.description}",
        StepStatusColumn("conversionStatus"),
        TextColumn("•"),
        BarColumn(),
        TextColumn(" "),
        MofNCompleteColumn(),
        TextColumn("•"),
        TimeElapsedColumn(),
        TextColumn("•"),
        ErrorCountColumn("errorCount")
    ) as progressBar:
        progressIds = {}
        for tableName, accessConversionDetails in tableConversionData.items():
            progressIds[tableName] = progressBar.add_task(
                tableName,
                conversionStatus=accessConversionDetails.conversionStatus,
                completed=accessConversionDetails.rowsConverted,
                total=accessConversionDetails.totalRows,
                errorCount=accessConversionDetails.errorCount
            )
        while True:
            try:
                message = logQueue.get(timeout=.1)
            except Empty:
                continue

            if message == "STOP":
                progressBar.stop()
                break

            # Expecting 3-tuple
            if isinstance(message, tuple) and len(message) == 2:
                (action, data) = message
                if action == "SET" or action == "RESET":
                    (tableName, total) = data
                    if total > 0:
                        progressBar.update(progressIds[tableName], conversionStatus="Not Started", completed=0, errorCount=0, total=total)
                    else:
                        progressBar.update(progressIds[tableName], conversionStatus="Complete", completed=0, errorCount=0, total=total)
                elif action == "UPDATE":
                    (tableName, conversionDetails) = data
                    targetProgress = progressIds[tableName]
                    if tableName in tableConversionData.keys():
                        numRowsConverted, numErrors = conversionDetails['rowsConverted'], conversionDetails['rowErrors']
                        task_obj = progressBar.tasks[targetProgress]

                        # Read built-in fields (these are attributes)
                        current_completed = task_obj.completed
                        current_total = task_obj.total

                        # Read custom fields from `fields` dict
                        current_error_count = task_obj.fields["errorCount"]

                        # Update your logic
                        errorCountTotal = current_error_count + numErrors
                        rowsConvertedTotal = current_completed + numRowsConverted

                        if rowsConvertedTotal == current_total:
                            conversionStatus = "Complete"
                        else:
                            conversionStatus = "In Progress"

                        # Finally, update the task
                        progressBar.update(
                            targetProgress, 
                            conversionStatus=conversionStatus,  # custom field
                            errorCount=errorCountTotal,         # custom field
                            completed=rowsConvertedTotal,       # built-in field
                        )
                    else:
                        console.print(f"[yellow]Unknown table: {tableName}[/yellow]")
                elif action == "ERROR":
                    progressBar.stop()
                    console.print(f"[red]{data}[/red]")
                    break
                elif action == "SUCCESS":
                    progressBar.stop()
                    console.print(f"[green]{data}[/green]")
                    break
                else:
                    progressBar.stop()
                    console.print(f"[red]Invalid Access conversion action: {action}[/red]")
                    break
            else:
                progressBar.stop()
                console.print(f"[red]Invalid Access conversion message: {message}[/red]")
                break