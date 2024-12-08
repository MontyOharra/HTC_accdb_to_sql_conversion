from ...imports import *

postalCodeFields: List[Field] = [
    Field(fieldName="id", fieldDetails="INTEGER PRIMARY KEY NOT NULL IDENTITY(1, 1)"),
    Field(fieldName="postal_code", fieldDetails="NVARCHAR(15) NOT NULL"),
]

postalCodeIndexes: List[Index] = [
]

postalCodeForeignKeys: List[ForeignKey] = [
]

def createPostalCodeTable(conn):
    postalCodeTable = SqlTable('postal_code', conn, postalCodeFields, postalCodeIndexes, postalCodeForeignKeys)
    postalCodeTable.createTable()
    postalCodeTable.addIndexes()

    return postalCodeTable