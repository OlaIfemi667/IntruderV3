from parsing.nmapParsing import *
from parsing.whoisParsing import *
from subprocessUtils.subprocess import *
from database.database import *

def ipAi(ip, scanName):
    print("[+] Nous avons puis joindre l'hôte")

    #faire un whois
    stdoutWhois, stderrWhois = asyncio.run(doWhois(ip))
    print(f"[+] Recherche enregistrement DNS de {ip} terminé")
    parsedWhois = whoisParsing(stderrWhois)
    print(parsedWhois)
    addProcesses(scanName, "whois", str(parsedWhois))



    
        
    #faire un scan de ports
    stdoutNmap, stderrNmap = asyncio.run(doNmap(ip))
    print(f"[+] Scan nmap de {ip}  terminé")
    parsedNmap = nmapParsing(f"{ip}Nmap.xml")
    addProcesses(scanName, "nmap", parsedNmap)


def searchspoitEveryService(nmapOutput):

    #reminder nmapOutput format
    #[
    #   {
    #       "ip": "aRandomIPaddress",
    #       "ports": [{"protocol": "TCP", "port": "80", "service": "HTTP"(or unknown if unknown), "product": "xxxx", "version": "2.1.0"}, "edb-ids": [list of EDB-ID]}],
    #       "os": {"name": "linux"}
    #   }
    #]

    exploits = []
    for port in nmapOutput["ports"]:
        for edcID in port["edb-id"]:
            #Logique pour récuperer le chemin de chaque exploit dans un  table et append {"portId": [list des chemins d'exploits]} dans la liste exploits
            # la commande pour  avoir des infos sur le path searchsploit -p 24450
            pass

        