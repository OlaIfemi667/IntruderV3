from parsing.nmapParsing import *
from parsing.whoisParsing import *
from parsing.nucleiParsing import *
from subprocessUtils.subprocess import *
from database.database import *
from zap.zap import *

async def ipAi(ip, scanName):

    # faire un whois
    stdoutWhois, stderrWhois = await doWhois(ip)
    print(f"[+] Recherche enregistrement DNS de {ip} terminé")
    parsedWhois = whoisParsing(stderrWhois)
    print(parsedWhois)
    addProcesses(scanName, "whois", str(parsedWhois))

    # faire un scan de ports
    stdoutNmap, stderrNmap = await doNmap(ip)
    print(f"[+] Scan nmap de {ip} terminé")
    
    addProcesses(scanName, "nmap", stdoutNmap)

    #faire le scan de vuln avec nuclei
    #stdoutNuclei, stderrNuclei = await nuclei(ip)
    #print(f"[+] Scan nuclei de {ip} terminé")
    
    #addProcesses(scanName, "nuclei", str(stdoutNuclei))


    # il faut que je code le systeme pour recherche les protocoles tcp web trouvé http, https
    zapOutput = zap(ip, "http")
    addProcesses(scanName, "zap", json.dumps(zapOutput, indent=4))



def vulnscan():
    pass


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

        