from src.classes.AccessConn import AccessConn

from src.types.types import Index

def getSqlTableIndexes(
    conn : AccessConn, 
    accessTableName : str
) -> list[Index]:
    '''
        conn - Access connection object.
        accessTableName - Name of the table to get the indexes for.
        
        Returns a list of Index objects representing the indexes in the table.
        
        TODO: Implement this
    '''
    return []
