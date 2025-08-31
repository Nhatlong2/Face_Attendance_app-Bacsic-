from services.db_service import DatabaseService

def main():
    db = DatabaseService()
    rows = db.fetchall("SELECT name FROM sys.databases")
    print("Danh sách databases trong SQL Server:")
    for r in rows:
        print("-", r[0])
    db.close()

if __name__ == "__main__":
    main()
