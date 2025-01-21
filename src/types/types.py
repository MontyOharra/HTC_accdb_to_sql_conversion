from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class Index:
    indexName: str
    indexFields: str | List[str]
    indexType: str
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
    tableName: str
    creationStatus: bool
    indexesStatus: bool
    
class accessConversionDetails:
    tableName: str
    