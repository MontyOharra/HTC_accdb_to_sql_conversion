from src.classes.AccessConn import AccessConn

from ...types import Field

def getSqlTableFields(
    conn : AccessConn, 
    accessTableName : str
) -> list[Field]:
    '''
        conn - Access connection object.
        accessTableName - Name of the table to get the fields for.
        
        Returns a list of Field objects representing the fields in the table.
        Forces all fields to be NOT NULL
    '''
    columnsInfo, primaryKeyColumns = conn.getTableStructure(accessTableName)
    fields = []
    
    for columnName, columnDetails in columnsInfo.items():
        fields.append(Field(columnName, columnDetails))
    
    return fields
