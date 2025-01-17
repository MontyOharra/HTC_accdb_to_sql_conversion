from threading import Thread
from queue import Queue, Empty
from typing import Dict

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
    
class StepStatusColumn(ProgressColumn):
    """A custom column to show the status of a given step (unstarted, working, completed)."""

    def __init__(self, step_name: str):
        super().__init__()
        self.step_name = step_name

    def render(self, task) -> Text:
        # Get the step status from the task fields
        step_status = task.fields.get(self.step_name, "Not Started")

        # You can define custom styling or coloring
        if step_status == "Not Started":
            style = "dim"
        elif step_status == "In Progress":
            style = "yellow"
        elif step_status == "Completed":
            style = "green"
        else:
            style = "red"

        return Text(step_status, style=style)    

class ErrorCountColumn(ProgressColumn):
    """A column that displays how many errors have occurred for a task."""
    
    def __init__(self, step_name: str):
        super().__init__()
        self.step_name = step_name
        
    def render(self, task) -> Text:
        errors = task.fields.get(self.step_name, 0)
        style = "green" if errors == 0 else "red"
        return Text(f"Conversion Errors: {errors}", style=style)
      
def printSqlCreationProgress(logQueue, tableData, successMessage):
    """
    Listens for messages like:
        ("sqlCreation", tableName, "status", "In Progress")
        ...
    Updates tablesData accordingly, rebuilds Rich tables, & calls live.update().
    """
    console = Console()
    
    with Progress(
        "[progress.description]{task.description}",
        StepStatusColumn("create"),
        TextColumn("•"),
        StepStatusColumn("index"),
    ) as progressBar:
        progressIds = {}
        for tableName in tableData.keys():
            progressIds[tableName] = progressBar.add_task(
                tableName
            )
        while True:
            try:
                message = logQueue.get(timeout=.1)
            except Empty:
                continue
            
            if message == "STOP":
                progressBar.stop()
                console.print("[red]Keyboard interrupt during SQL table creation. Stopping...[/red]")
                break
            
            if message == "COMPLETE":
                progressBar.stop()
                console.print(f"[green]{successMessage}[/green]")
                break

            # Expecting 4-tuple
            if isinstance(message, tuple) and len(message) == 3:
                (tableName, detailName, newValue) = message
                if tableName in tableData.keys():
                    if detailName == "creationStatus":
                        progressBar.update(progressIds[tableName], create=newValue)
                    elif detailName == "indexesStatus":
                        progressBar.update(progressIds[tableName], index=newValue)
                    else:
                        console.print(f"[yellow]Unknown detail: {detailName}[/yellow]")
                else:
                    console.print(f"[yellow]Unknown table: {tableName}[/yellow]")
            else:
                console.print(f"[red]Invalid message: {message}[/red]")
                

      
def printAccessConversionProgress(logQueue, tableData, successMessage):
    """
    Listens for messages like:
        ("sqlCreation", tableName, "status", "In Progress")
        ...
    Updates tablesData accordingly, rebuilds Rich tables, & calls live.update().
    """
    console = Console()
    
    with Progress(
        "[progress.description]{task.description}",
        StepStatusColumn("conversion"),
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
        for tableName in tableData.keys():
            progressIds[tableName] = progressBar.add_task(
                tableName
            )
        while True:
            try:
                message = logQueue.get(timeout=.1)
            except Empty:
                continue
            
            if message == "STOP":
                progressBar.stop()
                console.print("[red]Keyboard interrupt during Access table conversion. Stopping...[/red]")
                break
            
            if message == "COMPLETE":
                progressBar.stop()
                console.print(f"[green]{successMessage}[/green]")
                break
 
            # Expecting 4-tuple
            if isinstance(message, tuple) and len(message) == 3:
                (tableName, detailName, newValue) = message
                if tableName in tableData.keys():
                    if detailName == "conversionStatus":
                        progressBar.update(progressIds[tableName], conversion=newValue)
                    if detailName == "processedRows":
                        progressBar.advance(progressIds[tableName])
                    elif detailName == "totalRows":
                        progressBar.update(progressIds[tableName], total=newValue)
                    elif detailName == "errorCount":
                        progressBar.update(progressIds[tableName], errors=newValue)
                    else:
                        console.print(f"[yellow]Unknown detail: {detailName}[/yellow]")
                else:
                    console.print(f"[yellow]Unknown table: {tableName}[/yellow]")
            else:
                console.print(f"[red]Invalid message: {message}[/red]")
    


def processAndOutputData(
    connFactory, 
    conversionThreads, 
    printProgressFunction, 
    targetFunction,
    progressData : Dict[str, any],
    tableDefinitions : Dict[str, any],
    nonErrorMessage : str,
    errorMessage: str
):
    
    console = Console()
    logQueue = Queue()
    logThread = Thread(
        target=printProgressFunction,
        args=(logQueue, progressData, nonErrorMessage),
        daemon=True
    )
    logThread.start()
    
    try:
        targetFunction(
            connFactory, 
            logQueue, 
            tableDefinitions,
            maxThreads=conversionThreads
        )
        logQueue.put("COMPLETE")
    except KeyboardInterrupt:
        logQueue.put("STOP")
        raise KeyboardInterrupt
    except Exception as e:
        console.print(f"[red]{errorMessage}: {e}\n     {traceback.format_exc()}[/red]")
    finally:
        logQueue.put("END")
        logThread.join()

def splitAndProcessOutputData(
    connFactory, 
    conversionThreads, 
    printProgressFunction, 
    targetFunction,
    tableDefinitions : Dict[str, any],
    progressMessage : str,
    successMessage : str,
    errorMessage: str,
    maxProgressRowCount : int
):
    
    processesCompleted = 0
    processCount = len(tableDefinitions.keys())
    tableDefinitionsDivided = [dict(list(tableDefinitions.items())[i:i+maxProgressRowCount]) for i in range(0, len(tableDefinitions), maxProgressRowCount)]
    for tableDefinitionsSubset in tableDefinitionsDivided:  
        tablesCreationDataSubset = {
            tableName : {} for tableName in tableDefinitionsSubset.keys()
        }
        try:    
            processesCompleted += len(tableDefinitionsSubset)
            nonErrorMessage = f"{successMessage if processesCompleted == processCount else progressMessage} ({processesCompleted}/{processCount})"
            processAndOutputData(
                connFactory,
                conversionThreads,
                printProgressFunction,
                targetFunction,
                tablesCreationDataSubset,
                tableDefinitionsSubset,
                nonErrorMessage=nonErrorMessage,
                errorMessage=errorMessage
            )
        
        except KeyboardInterrupt:
            break
        
        