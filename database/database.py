import sqlite3
import sys


def init_db(db_path='database.db'):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS USER (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    groqApi TEXT,
                    zapApi TEXT
                );
                ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS SCANS (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    scanName TEXT NOT NULL UNIQUE,
                    ipaddress TEXT NOT NULL,
                    domain TEXT NOT NULL,
                    userId INTEGER,
                    date TEXT DEFAULT (datetime('now', 'localtime')),
                    FOREIGN KEY(userId) REFERENCES USER(id)
                );
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS PROCESSES (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    processType TEXT NOT NULL,
                    processOutput TEXT NOT NULL,
                    nameScan TEXT NOT NULL,
                    FOREIGN KEY(nameScan) REFERENCES SCANS(scanName)
                )
            ''')
            conn.commit()
        print("[+] database is ready is ready.")
    except sqlite3.Error as e:
        print(f"[!] Database error during initialization: {e}")


def addScan(name, ip, domain, db_path='database.db', id=None):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO SCANS (scanName, ipaddress, domain, userId) VALUES (?, ?, ?, ?)",
                (name, ip, domain, id)
            )
            conn.commit()
            print("[+] Scan ajouté avec succès.")
            return True
    except sqlite3.IntegrityError as e:
        print(f"[!] Erreur : Le nom de scan '{name}' existe déjà. Veuillez en choisir un autre.")
        sys.exit(1) 
    except sqlite3.Error as e:
        print(f"[!] Erreur base de données: {e}")
    except Exception as e:
        print(f"[!] Erreur inattendue: {e}")
    return False

def checkScanExists(name, db_path='database.db'):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM SCANS WHERE scanName = ?", (name,))
            count = cursor.fetchone()[0]
            return count > 0
    except sqlite3.Error as e:
        print(f"[!] Database error: {e}")
    except Exception as e:
        print(f"[!] Unexpected error: {e}")
    return False


def addProcesses(nameScan, typeOutput, output, db_path = 'database.db'):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO PROCESSES (processType, processOutput, nameScan) VALUES (?, ?, ?)",
                (typeOutput, output, nameScan)
            )
            conn.commit()
            print("Process ADDEDDDDDDDDDDD")
    except sqlite3.Error as e:
        print(f"[!] Database error: {e}")
    except Exception as e:
        print(f"[!] Unexpected error: {e}")
    return False



def getScans(db_path='database.db', userId=None):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT scanName FROM SCANS where userId = ?", (userId,))
            rows = cursor.fetchall()
            print(f"{rows}AAAAAAAAAAAAAAAAAAAAAAAA")
            return [row[0] for row in rows]  
    except sqlite3.Error as e:
        print(f"[!] Database error: {e}")
    except Exception as e:
        print(f"[!] Unexpected error: {e}")
    return ["default"]


def getScansDetails(db_path='database.db', scanName="default", id=None):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * from PROCESSES where nameScan = ?  ", (scanName,))
            rows = cursor.fetchall()
            print(len(rows))
            return rows
    
    except sqlite3.Error as e:
        print(f"[!] Database error: {e}")
    except Exception as e:
        print(f"[!] Unexpected error: {e}")
    return ["default"]


