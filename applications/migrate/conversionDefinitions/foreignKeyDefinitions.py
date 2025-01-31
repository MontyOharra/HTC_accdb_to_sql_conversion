from src.classes.AccessConn import AccessConn

from src.types.types import ForeignKey

def getSqlTableForeignKeys(
    conn : AccessConn, 
    accessTableName : str
) -> list[ForeignKey]:
    '''
        conn - Access connection object.
        accessTableName - Name of the table to get the foreign keys for. 
        
        Returns a list of ForeignKey objects representing the foreign keys in the table.
        
        TODO: Implement this
    '''
    return []