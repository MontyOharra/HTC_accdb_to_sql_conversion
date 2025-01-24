from .AccessConn import AccessConn
from .SqlServerConn import SqlServerConn

class ConnFactory:
    def __init__(self, sqlDriver, sqlServerName, sqlDatabaseName, htcAllPath):
        self.sqlDriver = sqlDriver
        self.sqlServerName = sqlServerName
        self.sqlDatabaseName = sqlDatabaseName
        self.htcAllPath = htcAllPath

    def sql(self):
        """Return a new SqlServerConn."""
        return SqlServerConn(self.sqlDriver, self.sqlServerName, self.sqlDatabaseName)

    def htc000(self):
        return AccessConn(self.htcAllPath, 'HTC000_Data_Staff.accdb')

    def htc010(self):
        return AccessConn(self.htcAllPath, 'HTC010_Static_data.accdb')

    def htc300(self):
        return AccessConn(self.htcAllPath, 'HTC300_Data-01-01.accdb')

    def htc301(self):
        return AccessConn(self.htcAllPath, 'HTC301_Data_Change_Log.accdb')

    def htc320(self):
        return AccessConn(self.htcAllPath, 'HTC320_TSA_Data-01-01.accdb')

    def htc321(self):
        return AccessConn(self.htcAllPath, 'HTC321_TSA Data Change Log.accdb')

    def htc350d(self):
        return AccessConn(self.htcAllPath, 'HTC350D ETO Parameters.accdb')

    def htc350(self):
        return AccessConn(self.htcAllPath, 'HTC350D_Database.accdb')

    def htc400Archive(self):
        return AccessConn(self.htcAllPath, 'HTC400_Order Archives.accdb')

    def htc400(self):
        return AccessConn(self.htcAllPath, 'HTC400_Order Archive DB-01-01.accdb')