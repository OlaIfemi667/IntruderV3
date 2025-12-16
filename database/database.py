import sqlite3
import sys
import os


# Chemin absolu unique vers la base SQLite, aligné avec app/__init__.py
base_dir = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(base_dir, '..', 'database.db')


def init_db(db_path=DB_PATH):
    #Au niveau de Util l'attribut type est "default" pour les outils supporter de base et donc pour 
    #lesquels on a un process de parsing ou "added" pour les outils custom
    #processType c'est le nom de l'outil
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
                    userId INTEGER,
                    FOREIGN KEY(nameScan) REFERENCES SCANS(scanName),
                    FOREIGN KEY(userId) REFERENCES USER(id)
                )
            ''') 
            conn.commit()
        print("[+] database is ready is ready.")
    except sqlite3.Error as e:
        print(f"[!] Database error during initialization: {e}")


def insertBuiltinTools(db_path=DB_PATH):
    tools = [
        ("Nmap", "Outil de scan de réseau et de sécurité", "default"),
        ("Nikto", "Scanner de vulnérabilités web", "default"),
        ("Gobuster", "Outil de brute force pour découvrir des ressources web", "default"),
        ("Dirb", "Outil de brute force pour découvrir des répertoires web", "default"),
    ]

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.executemany(
                "INSERT OR IGNORE INTO UTIL (name, description, Utiltype) VALUES (?, ?, ?)",
                tools
            )
            conn.commit()
            print("[+] Outils par défaut insérés avec succès.")
    except sqlite3.Error as e:
        print(f"[!] Erreur lors de l'insertion des outils : {e}")


def addScan(name, ip, domain, db_path=DB_PATH, id=None):
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
    except sqlite3.Error as e:
        print(f"[!] Erreur base de données: {e}")
    except Exception as e:
        print(f"[!] Erreur inattendue: {e}")
    return False


def checkScanExists(name, db_path=DB_PATH):
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


def addProcesses(nameScan, typeOutput, output, db_path=DB_PATH):
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


def getanUsername(userId=None, db_path=DB_PATH):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM USER WHERE id = ?", (userId,))
            row = cursor.fetchone()
            if row:
                return row[0]
            else:
                print(f"[!] No user found with ID {userId}")
                return None
    except sqlite3.Error as e:
        print(f"[!] Database error: {e}")
    except Exception as e:
        print(f"[!] Unexpected error: {e}")
    return None


def getAllScans(db_path=DB_PATH):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT scanName, userID, id FROM SCANS")
            rows = cursor.fetchall()
            return [{"scanName": row[0], "userId": row[1], "id": row[2]} for row in rows]
    except sqlite3.Error as e:
        print(f"[!] Database error: {e}")


def getScansDetails(db_path=DB_PATH, scanName="default", userId=None):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            if userId is not None:
                cursor.execute(
                    "SELECT * from PROCESSES where nameScan = ? AND userId = ?",
                    (scanName, userId),
                )
            else:
                # Fallback ancien comportement si aucun userId n'est fourni
                cursor.execute(
                    "SELECT * from PROCESSES where nameScan = ?",
                    (scanName,),
                )
            rows = cursor.fetchall()
            print(len(rows))
            return rows
    
    except sqlite3.Error as e:
        print(f"[!] Database error: {e}")
    except Exception as e:
        print(f"[!] Unexpected error: {e}")
    return ["default"]


def getScanStatus(scanName, userId, db_path=DB_PATH):
    """
    Retourne un statut simple pour un scan donné et un utilisateur :
    - 'pending'  : aucun résultat en base
    - 'running'  : au moins un process (ex: Nmap) mais pas encore ZAP
    - 'finished' : ZAP présent
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT processType FROM PROCESSES WHERE nameScan = ? AND userId = ?",
                (scanName, userId),
            )
            rows = cursor.fetchall()

        if not rows:
            return "pending"

        types = {row[0] for row in rows}
        if "zap" in types:
            return "finished"
        return "running"

    except sqlite3.Error as e:
        print(f"[!] Database error in getScanStatus: {e}")
    except Exception as e:
        print(f"[!] Unexpected error in getScanStatus: {e}")
    return "unknown"



