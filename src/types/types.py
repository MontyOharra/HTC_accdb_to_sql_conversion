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
    
@dataclass
class SqlCreationDetails:
    creationStatus: str
    indexesStatus: str
    
class accessConversionDetails:
    tableName: str
    