from typing import List

import re

def createFieldsArrayFromString(fieldsString : str) -> str:
    # Regex pattern to match field definitions
    pattern = r"\[\s*(\w+)\s*\]\s+([^\n,]+)"

    matches = re.findall(pattern, fieldsString)

    # Format matches into the desired output
    fields = [
        f'Field(fieldName="{field_name}", fieldDetails="{field_details.strip()}")'
        for field_name, field_details in matches
    ]

    # Print the result in the desired format
    return "addressFields: List[Field] = [\n    " + ",\n    ".join(fields) + "\n]"

def createIndexArrayFromString():
    pass