from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

def getAccessDbName(tableName):
    if tableName == 'HTC400_G900_T010 Archive Event Log':
        return 'htc400archive'
    else:
        return tableName[0:6].lower()

def getRows(connFactory, tableName):
    localConn = connFactory()
    rows = localConn.accessGetTableInfo(getAccessDbName(tableName), tableName)
    localConn.close()
    return rows
  
def createSqlTable(connFactory, tableName, tableFields, tableIndexes, sqlCreationLogQueue):
    # Mark table in progress
    sqlCreationLogQueue.put((tableName, "creationStatus", "In Progress"))
    sqlCreationLogQueue.put((tableName, "indexesStatus", "In Progress"))
    localConn = None
    try:
        localConn = connFactory()
        sqlCreationLogQueue.put((tableName, "startTime", str(datetime.now())))
        try:
            localConn.sqlCreateTable(tableName, tableFields)
            sqlCreationLogQueue.put((tableName, "creationStatus", "Completed"))
        except Exception as err:
            sqlCreationLogQueue.put((tableName, "creationStatus", "Failure"))
        
        try:
            for index in tableIndexes:
                localConn.sqlAddIndex(tableName, index.indexType, index.indexFields, index.indexName, index.isUnique)
            sqlCreationLogQueue.put((tableName, "indexesStatus", "Completed"))
        except Exception as err:
            sqlCreationLogQueue.put((tableName, "indexesStatus", "Failure"))
        sqlCreationLogQueue.put((tableName, "endTime", str(datetime.now())))
        
    except Exception as err:
        sqlCreationLogQueue.put(("sqlCreation", tableName, "creationStatus", "Failure"))
        sqlCreationLogQueue.put((tableName, "indexesStatus", "Failure"))
        # logError("error.log", f"SQL Table: {tableName}, Error: {err}")
    finally:
        if localConn:
            localConn.close()

def createSqlTables(connFactory, sqlCreationLogQueue, sqlTableDefinitions, maxThreads = 1): 
    with ThreadPoolExecutor(maxThreads) as executor:
        futures = [
            executor.submit(
                createSqlTable, 
                connFactory, 
                tableName,
                fields,
                indexes,
                sqlCreationLogQueue
            )
            for tableName, (fields, indexes, fks) in sqlTableDefinitions.items()
        ]
        for future in as_completed(futures):
            future.result()


def convertAccessTable(connFactory, accessConversionLogQueue, tableName, rows, rowConversion): 
    # Mark table in progress
    if not rows:
        accessConversionLogQueue.put((tableName, "status", "Empty"))
        accessConversionLogQueue.put((tableName, "totalRows", 0))
        return
    
    try:
        localConn = connFactory()
        accessConversionLogQueue.put((tableName, "status", "Incomplete"))
        accessConversionLogQueue.put((tableName, "totalRows", len(rows)))
        accessConversionLogQueue.put((tableName, "startTime", str(datetime.now())))
        
        processedRows = 0
        errorCount = 0 
        
        for row in rows:
            try:
                rowConversion(localConn, row)
            except Exception as err:
                errorCount += 1
                # IMPLEMENT LOGGING FUNCTIONALITY
                # print(err)
                accessConversionLogQueue.put((tableName, "errorCount", errorCount))
                continue
            finally:
                processedRows += 1
                accessConversionLogQueue.put((tableName, "processedRows", processedRows))
        
        accessConversionLogQueue.put((tableName, "endTime", str(datetime.now())))
        accessConversionLogQueue.put((tableName, "status", "Complete"))
            
    except Exception as err:
        accessConversionLogQueue.put(("sqlCreation", tableName, "status", "Failure"))
    finally:
        if localConn:
            localConn.close()

def convertAccessTables(connFactory, accessConversionLogQueue, accessConversionDefinitions, maxThreads = 1): 
    with ThreadPoolExecutor(maxThreads) as executor:
        futures = [
            executor.submit(
                convertAccessTable, 
                connFactory,
                accessConversionLogQueue, 
                tableName,
                getRows(connFactory, tableName),
                rowConversionFunction
            )
            for tableName, rowConversionFunction in accessConversionDefinitions.items()
        ]
        for future in as_completed(futures):
            future.result()