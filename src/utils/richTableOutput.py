from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.text import Text

import queue 

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
        elif step_status == "Complete":
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
      
def outputSqlCreationLoggingProgress(logQueue, tableData, successMessage):
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
        StepStatusColumn("index")
    ) as progressBar:
        progressIds = {}
        for tableName in tableData.keys():
            progressIds[tableName] = progressBar.add_task(
                tableName
            )
        while True:
            try:
                message = logQueue.get(timeout=1)
            except queue.Empty:
                continue
            
            if message == "STOP":
                progressBar.stop()
                console.print("[red]Keyboard interrupt during SQL table creation. Stopping...[/red]")
                break
            
            if message == "COMPLETE":
                progressBar.stop()
                console.print(f"[green]{successMessage}[/green]")
                
            if message == "END":
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
                

      
def outputAccessConversionLoggingProgress(logQueue, tableData, successMessage):
    """
    Listens for messages like:
        ("sqlCreation", tableName, "status", "In Progress")
        ...
    Updates tablesData accordingly, rebuilds Rich tables, & calls live.update().
    """
    console = Console()
    print("Starting this shit")
    
    with Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        TextColumn("•"),
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
        try:
            while True:
                try:
                    message = logQueue.get(timeout=1)
                except:
                    continue
                
                if message == "STOP":
                    progressBar.stop()
                    break

                # Expecting 4-tuple
                if isinstance(message, tuple) and len(message) == 3:
                    (tableName, detailName, newValue) = message
                    if tableName in tableData.keys():
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
                    
            console.print(f"[green]{successMessage}[/green]")
        except KeyboardInterrupt:
            console.print("[red]Keyboard interrupt during SQL table creation. Stopping...[/red]") 

            # Expecting 4-tuple
            if isinstance(message, tuple) and len(message) == 3:
                (tableName, detailName, newValue) = message
                if tableName in tableData.keys():
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

    console.print(f"[green]{successMessage}[/green]")
    