import json
from parsing.nmapParsing import *
from parsing.whoisParsing import *
from parsing.nucleiParsing import *
from subprocessUtils.subprocess import *
from database.database import *
from zap.zap import *
from traductionAndNotification.traduction import translate_en_fr


async def ipAi(ip, scanName, domain, id=None, zapApiKey=None):
    """
    Lance les différents scans (Nmap, ZAP, etc.) et enregistre les résultats en base.
    Cette fonction est appelée dans un thread séparé depuis la vue Flask.
    """

    try:
        # ---- Scan Nmap ----
        stdoutNmap, stderrNmap = await doNmap(ip)
        if stderrNmap:
            print(f"[!] Erreur lors du scan Nmap pour {ip}: {stderrNmap}")
            return

        print(f"[+] Scan Nmap pour {ip} terminé")
        print("[+] Ajout des résultats Nmap dans la base")
        addProcesses(scanName, "nmap", stdoutNmap)



        # ---- Création de l'entrée de scan globale ----
        print(f"[+] Enregistrement du scan '{scanName}' pour l'utilisateur {id}")
        added = addScan(scanName, ip, domain, id=id)
        if not added:
            print(f"[!] Impossible d'enregistrer le scan '{scanName}' (doublon ou erreur DB)")
            # On peut continuer les scans, mais on log le problème

        # ---- Scan ZAP ----
        try:
            print(f"[+] Lancement du scan ZAP sur {ip}")
            zapOutput = zap(ip, "http", zapApiKey)  # adapter si besoin le schéma/proto
            
            # Ajouter la traduction française de la description pour chaque alerte
            if zapOutput and isinstance(zapOutput, list):
                for alert in zapOutput:
                    if isinstance(alert, dict) and 'description' in alert:
                        try:
                            alert['description_fr'] = translate_en_fr(alert['description'])
                            print(f"[+] Description traduite pour l'alerte: {alert.get('name', 'Unknown')}")
                        except Exception as e:
                            print(f"[!] Erreur lors de la traduction de la description: {e}")
                            # En cas d'erreur, on garde la description originale
                            alert['description_fr'] = alert.get('description', '')
            
            addProcesses(scanName, "zap", json.dumps(zapOutput, indent=4))
            print(f"[+] Scan ZAP sur {ip} terminé et enregistré")
        except Exception as e:
            print(f"[!] Erreur lors du scan ZAP pour {ip}: {e}")

        print(f"[+] Pipeline ipAi terminé pour le scan '{scanName}' ({ip})")

    except Exception as e:
        # Catch global pour éviter qu'une exception ne tue silencieusement le thread
        print(f"[!] Erreur inattendue dans ipAi pour le scan '{scanName}' ({ip}): {e}")
