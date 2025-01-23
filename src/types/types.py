from dataclasses import dataclass
from typing import List, Dict, Any, Literal

ValidIndexType = Literal['clustered', 'nonclustered']

@dataclass
class Index:
    indexName: str
    indexFields: str | List[str]
    indexType: ValidIndexType
    isUnique: bool
    
@dataclass
class ForeignKey:
    fromTableName: str
    fromTableField: str
    toTableName: str
    toTableField: str

@dataclass
class Field:
    fieldName: str
    fieldDetails: str
    
status = Literal["In Progress", "Complete", "Failure", "Not Started"]
@dataclass
class SqlCreationDetails:
    creationStatus: status
    indexesStatus: status
    
@dataclass
class AccessConversionDetails:
    conversionStatus: status
    totalRows: int
    rowsConverted: int
    errorCount: int