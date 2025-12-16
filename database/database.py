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
                    FOREIGN KEY(nameScan) REFERENCES SCANS(scanName)
                )
            ''') 
            conn.commit()
        print("[+] database is ready is ready.")
    except sqlite3.Error as e:
        print(f"[!] Database error during initialization: {e}")





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


def addProcesses(nameScan, typeOutput, output, userId=None, db_path=DB_PATH):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO PROCESSES (processType, processOutput, nameScan, userId) VALUES (?, ?, ?, ?)",
                (typeOutput, output, nameScan, userId)
            )
            conn.commit()
            print(f"[+] Process {typeOutput} ajouté pour le scan {nameScan}")
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
    """
    Récupère les détails d'un scan. Si userId est fourni, filtre par userId.
    Si aucun résultat avec userId, essaie sans userId (pour compatibilité avec anciens scans).
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            if userId is not None:
                # D'abord, chercher avec userId
                cursor.execute(
                    "SELECT * from PROCESSES where nameScan = ? AND userId = ?",
                    (scanName, userId),
                )
                rows = cursor.fetchall()
                # Si aucun résultat avec userId, essayer sans userId (anciens scans)
                if not rows:
                    cursor.execute(
                        "SELECT * from PROCESSES where nameScan = ?",
                        (scanName,),
                    )
                    rows = cursor.fetchall()
            else:
                # Fallback ancien comportement si aucun userId n'est fourni
                cursor.execute(
                    "SELECT * from PROCESSES where nameScan = ?",
                    (scanName,),
                )
                rows = cursor.fetchall()
            
            print(f"[+] getScansDetails: {len(rows)} processus trouvés pour le scan '{scanName}'")
            return rows
    
    except sqlite3.Error as e:
        print(f"[!] Database error: {e}")
    except Exception as e:
        print(f"[!] Unexpected error: {e}")
    return []


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
            # D'abord chercher avec userId
            cursor.execute(
                "SELECT processType FROM PROCESSES WHERE nameScan = ? AND userId = ?",
                (scanName, userId),
            )
            rows = cursor.fetchall()
            
            # Si aucun résultat avec userId, essayer sans userId (anciens scans)
            if not rows:
                cursor.execute(
                    "SELECT processType FROM PROCESSES WHERE nameScan = ?",
                    (scanName,),
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



