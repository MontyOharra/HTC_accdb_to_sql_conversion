from dataclasses import dataclass

@dataclass
class Index:
    indexName: str
    indexType: str
    indexField: str
    isUnique: bool