from collections import defaultdict
from queue import Queue, Empty
import os
import json
from dataclasses import asdict

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

from typing import Any
from src.types import SqlCreationDetails, AccessConversionDetails, status
    
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

def createLogFile(htcConversionLogPath : str) -> None:
    with open(htcConversionLogPath, "w") as logFile:
        json.dump({
            "sqlCreation": {}, 
            "accessConversion": {}, 
            "errors" : {
              "sqlCreation": [], 
              "accessConversion": [], 
              "other": []
            }},
            logFile)
    
def readSqlCreationLog(htcConversionLogPath : str) -> dict[str, SqlCreationDetails] | None:
    '''
        logDir - The directory where the logs are stored.
        
        Returns a dictionary of the logs, where the key is the table name and the value is the log details.
        If the log file does not exist, returns None.
    '''
    # Log file does not exist
    with open(htcConversionLogPath) as htcConversionLogFile:        
        data = json.load(htcConversionLogFile)
        # There is not sqlCreation data
        if not data['sqlCreation']:
            return None
        sqlCreationLogs = data["sqlCreation"]
        for tableName, sqlCreationDetails in sqlCreationLogs.items():
            sqlCreationLogs[tableName] = SqlCreationDetails(
                sqlCreationDetails['creationStatus'],
                sqlCreationDetails['indexesStatus']
            )
        return sqlCreationLogs

def readAccessConversionLog(htcConversionLogPath : str) -> dict[str, AccessConversionDetails] | None:
    if not os.path.exists(htcConversionLogPath):
        return None
    with open(htcConversionLogPath) as htcConversionLogFile:        
        data = json.load(htcConversionLogFile)
        # There is not sqlCreation data
        if not data['accessConversion']:
            return None
        accessConversionLogs = data["accessConversion"]
        for tableName, accessConversionDetails in accessConversionLogs.items():
            accessConversionLogs[tableName] = AccessConversionDetails(
                accessConversionDetails['conversionStatus'],
                accessConversionDetails['totalRows'],
                accessConversionDetails['rowsConverted'],
                accessConversionDetails['errorCount']
            )
        return accessConversionLogs

def writeErrorLog(logPath : str, errors : dict[str, list[str]]) -> None:
    '''
        logPath - The path to the log file.
        errors - A dictionary of errors, where the keys are the process names and the values are the error messages.
    '''
    with open(logPath, "r") as f:
        data = json.load(f)
    errorData = data['errors']
    for process, error in errors.items():
        errorData[process].append(error)
        
    with open(logPath, "w") as htcConversionLogFile:
        json.dump({
          "sqlCreation": data['sqlCreation'],
          "accessConversion": data['accessConversion'],
          "errors": errorData
        }, htcConversionLogFile, indent=4)
      
        
def logErrors(errorLogQueue: Queue, logPath: str):
    console = Console()

    with open(logPath, "r") as f:
        data = json.load(f)

    errors = {
      'sqlCreation': [],
      'accessConversion': [],
      'other': []
    }
    while True:
        try:
            message = errorLogQueue.get(timeout=0.1)
        except Empty:
            continue
        if message == "STOP":
            break

        # Expecting a tuple: (process, exception).
        if isinstance(message, tuple) and len(message) == 2:        
            process, exception = message
            errors[process].append(str(exception))
        else:
            console.print(f"[red]Invalid message: {message}[/red]")

    writeErrorLog(logPath, errors)
  
def writeSqlCreationLog(logPath : str, newSqlCreationData : dict[str, SqlCreationDetails]) -> None:
    with open(logPath, "r") as f:
        data = json.load(f)
    sqlCreationData = data['sqlCreation']
        
    for tableName, sqlCreationDetails in newSqlCreationData.items():
        # Update old values with new values if they are in the same table
        sqlCreationDict = asdict(sqlCreationDetails)
        sqlCreationData[tableName] = sqlCreationDict
        
    with open(logPath, "w") as htcConversionLogFile:
        json.dump({
          "sqlCreation": sqlCreationData,
          "accessConversion": data['accessConversion'],
          "errors": data['errors']
        }, htcConversionLogFile, indent=4)
            
def logSqlCreationProgress(
    logQueue : Queue,
    tableCreationData : dict[str, SqlCreationDetails],
    logPath : str
):
    """
        Listens for messages sent in from a Queue object.
        Returns true if the process is complete., false otherwise.
        
        logQueue - Queue object to listen for messages from.
        tableCreationData - Dictionary of table names and their status.
        logDir - Directory to log the progress to.
    """
    console = Console()
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
                if action == "BEGIN":
                    (tableName) = data
                    progressBar.update(progressIds[tableName], creationStatus="Not Started", indexesStatus="Not Started")
                elif action == "UPDATE":
                    (tableName, sqlCreationDetails) = data
                    if tableName in tableCreationData.keys():
                        tableCreationData[tableName] = sqlCreationDetails
                        progressBar.update(progressIds[tableName], 
                                           creationStatus=sqlCreationDetails.creationStatus, 
                                           indexesStatus=sqlCreationDetails.indexesStatus
                                          )
                    else:
                        console.print(f"[yellow]Unknown table: {tableName}[/yellow]")
                elif action == "ERROR":
                    console.print(f"[red]{data}[/red]")
                    break   
                elif action == "SUCCESS":
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
              
    writeSqlCreationLog(logPath, tableCreationData)
        
def writeAccessConversionLog(logPath : str, newAccessConversionData : dict[str, AccessConversionDetails]) -> None:
    with open(logPath, "r") as f:
        data = json.load(f)
    
    accessConversionData = data['accessConversion']
        
    for tableName, accessConversionDetails in newAccessConversionData.items():
        # Update old values with new values if they are in the same table
        accessConversionDict = asdict(accessConversionDetails)
        accessConversionData[tableName] = accessConversionDict
        
    with open(logPath, "w") as htcConversionLogFile:
        json.dump({
          "sqlCreation": data['sqlCreation'],
          "accessConversion": accessConversionData,
          "errors": data['errors']
        }, htcConversionLogFile, indent=4)
        
def logAccessConversionProgress(
    logQueue : Queue,
    tableConversionData : dict[str, AccessConversionDetails],
    logPath : str
) -> None:
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
        ErrorCountColumn("errorCount"),                
        refresh_per_second=10,
        transient=False
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
                if action == "BEGIN":
                    (tableName, total) = data
                    if total > 0:
                        conversionDetails = AccessConversionDetails("Not Started", total, 0, 0)
                    else:
                        conversionDetails = AccessConversionDetails("Empty Table", total, 0, 0)
                    tableConversionData[tableName] = conversionDetails
                    progressBar.update(progressIds[tableName], conversionStatus=conversionDetails.conversionStatus, completed=0, errorCount=0, total=total)
                elif action == "UPDATE":
                    (tableName, conversionProgress) = data
                    targetProgress = progressIds[tableName]
                    if tableName in tableConversionData.keys():
                        task_obj = progressBar.tasks[targetProgress]

                        current_completed = task_obj.completed
                        current_total = task_obj.total
                        current_error_count = task_obj.fields["errorCount"]

                        errorCountTotal = current_error_count + conversionProgress['rowErrors']
                        rowsConvertedTotal = current_completed + conversionProgress['rowsConverted']

                        if rowsConvertedTotal == current_total:
                            conversionStatus = "Complete"
                        else:
                            conversionStatus = "In Progress"
                        tableConversionData[tableName].conversionStatus = conversionStatus
                        tableConversionData[tableName].rowsConverted = rowsConvertedTotal
                        tableConversionData[tableName].errorCount = errorCountTotal

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
              
    writeAccessConversionLog(logPath, tableConversionData)