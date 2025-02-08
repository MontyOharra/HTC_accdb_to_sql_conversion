from typing import Any

def getNullReplacement(
    fieldType : str
) -> Any:
    if fieldType in ('int', 'float', 'decimal'):
        return 0
    elif fieldType in ('nvarchar', 'varchar', 'ntext', 'text'):
        return ''