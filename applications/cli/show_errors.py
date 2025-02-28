import json
import os
from glob import glob
from typing import Any


def get_latest_log_file() -> str | None:
    """Get the path of the most recent log file"""
    log_files = glob("logs/htcConversion-*.json")
    if not log_files:
        return None
    return max(log_files, key=os.path.getctime)


def format_error_message(error: str) -> str:
    """Convert string with literal newlines and escaped quotes to actual newlines and quotes"""
    return error.replace("\\n", "\n").replace("\\'", "'")


def print_error_section(section_name: str, errors: list[Any]) -> None:
    """Print a section of errors with proper formatting"""
    print(f"\n{section_name}:")
    if not errors:
        print("No errors found")
        return

    for err in errors:
        if isinstance(err, str):
            print(f"\nError: {format_error_message(err)}")
        elif err:
            print(f"\nError: {format_error_message(str(err))}")


def display_errors(log_file: str) -> None:
    """Display all errors from the given log file"""
    try:
        with open(log_file, "r") as f:
            data = json.load(f)

        print(f"\nDisplaying errors from: {log_file}\n")

        print_error_section("SQL Creation Errors", data["errors"]["sqlCreation"])
        print_error_section(
            "Access Conversion Errors", data["errors"]["accessConversion"]
        )
        print_error_section("Other Errors", data["errors"]["other"])

    except Exception as e:
        print(f"Error reading log file: {str(e)}")
        raise  # This will help us see the full error trace during development


def main():
    log_file = get_latest_log_file()
    if not log_file:
        print("No log files found in logs directory")
        return
    display_errors(log_file)


if __name__ == "__main__":
    main()
