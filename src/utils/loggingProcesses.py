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
        if message == "COMPLETE":
            break
          
        # Write error to error.log file within the same directory as the script
        # Error of the type (process, tableName, errorMessage)
        # Expecting 4-tuple
        if isinstance(message, tuple) and len(message) == 3:        
            with open(f"{os.path.dirname(os.path.abspath(__file__))}/error.log", "a") as errorLogFile:
                errorLogFile.write(f"Current process: {message[0]}\n    Table: {message[1]}\n        Error: {message[2]}\n")
        else:
            console.print(f"[red]Invalid message: {message}[/red]")
    
        
        
def logSqlCreationProgress(
    logQueue : Queue,
    tableCreationData : Dict[str, SqlCreationDetails]
) -> bool:
    """
        Listens for messages sent in from a Queue object.
        Returns true if the process is complete., false otherwise.
        
        logQueue - Queue object to listen for messages from.
        tableData - Dictionary of table names and their status.
        successMessage - Message to display when the process is complete.
    """
    console = Console()
    with Progress(
            "[progress.description]{task.description}",
            StepStatusColumn("creationStatus"),
            TextColumn("•"),
            StepStatusColumn("indexesStatus"),
            refresh_per_second=10
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
                if action == "UPDATE":
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
                    progressBar.update(progressIds[tableName], completed=0, errorCount=0, total=total)
                if action == "UPDATE":
                    (tableName, sqlCreationDetails) = data
                    if tableName in tableConversionData.keys():
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
) :
    
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
        
        