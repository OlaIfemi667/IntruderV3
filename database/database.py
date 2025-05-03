import sqlite3


def init_db(db_path='database.db'):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS scannerOutput (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL,
                    output TEXT NOT NULL
                )
            ''')
            conn.commit()
        print("[+] Table 'scannerOutput' is ready.")
    except sqlite3.Error as e:
        print(f"[!] Database error during initialization: {e}")


def addScannerOutput(scan_type, output, db_path='database.db'):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO scannerOutput (type, output) VALUES (?, ?)",
                (scan_type, output)
            )
            conn.commit()
    except sqlite3.Error as e:
        print(f"[!] Database error: {e}")
    except Exception as e:
        print(f"[!] Unexpected error: {e}")
    return output
