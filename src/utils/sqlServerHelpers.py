import pyodbc
import winreg
import socket

def get_local_sql_server_instances():
    instances = []

    try:
        # Define the registry key path
        key_path = r"SOFTWARE\Microsoft\Microsoft SQL Server\Instance Names\SQL"
        
        # Open the registry key
        try:
            # Try accessing the 64-bit registry view first
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0,
                                 winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
        except FileNotFoundError:
            # Fall back to the 32-bit registry view
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ)
        
        # Enumerate the instances
        i = 0
        while True:
            try:
                instance_name = winreg.EnumValue(key, i)[0]
                instances.append(instance_name)
                i += 1
            except OSError:
                break  # No more instances
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Error accessing the registry: {e}")

    return instances

def getAllSqlServerNames(instance_name):
    hostname = socket.gethostname()
    
    if instance_name == "MSSQLSERVER":
        server_name = hostname  # Default instance
    else:
        server_name = f"{hostname}\\{instance_name}"  # Named instance
    
    return server_name

def getSqlServerName():
    # Get SQL Server instances
    sql_instances = get_local_sql_server_instances()
    if not sql_instances:
        print("There are no sql servers on this machine. Please setup a server and retry the converion. \n [ABORTING CONVERSION PROCCESS]")
        return None
        # Attempt to connect to each instance
    if len(sql_instances) == 1:
        instance = sql_instances[0]
        return getAllSqlServerNames(instance)
    else:
        print("There are more than one sql servers on this machine. Please choose the server you would like to target:")
        for index, instance in enumerate(sql_instances):
            print(f"{getAllSqlServerNames(instance)} [{index}]" )
        instanceNum = int(input("Type the number next to the server instance you would like to select"))
        return (getAllSqlServerNames(instance[instanceNum]))
    
def checkIfDatabaseExists(sqlCursor, databaseName):
    check_db_query = """
    SELECT 1 FROM sys.databases WHERE name = ?
    """
    sqlCursor.execute(check_db_query, (databaseName,))
    return sqlCursor.fetchone() is not None

def createDatabase(sqlCursor, databaseName):
    create_db_query = f"CREATE DATABASE [{databaseName}]"
    try:
        sqlCursor.execute(create_db_query)
        print(f"Database '{databaseName}' created successfully.")
    except pyodbc.Error as ex:
        print(f"Failed to create database '{databaseName}': {ex}")
        exit(1)
