from dataclasses import dataclass

from typing import List

@dataclass
class Index:
    indexName: str
    indexFields: str | List[str]
    indexType: str
    isUnique: bool