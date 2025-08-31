import pyodbc
from utils.config import DB_CONFIG

class DatabaseService:
    def __init__(self):
        server = DB_CONFIG["server"]
        database = DB_CONFIG["database"]
        auth = DB_CONFIG["auth"]

        if auth == "sql":
            username = DB_CONFIG["username"]
            password = DB_CONFIG["password"]
            conn_str = f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
        else:
            conn_str = f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"

        self.conn = pyodbc.connect(conn_str)
        self.cursor = self.conn.cursor()

    def execute(self, query, params=None):
        self.cursor.execute(query, params or [])
        self.conn.commit()

    def fetchall(self, query, params=None):
        self.cursor.execute(query, params or [])
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
