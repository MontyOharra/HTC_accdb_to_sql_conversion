from dataclasses import dataclass

@dataclass
class ForeignKey:
    fromTableName: str
    fromTableField: str
    toTableName: str
    toTableField: str