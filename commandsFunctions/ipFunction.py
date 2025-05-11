from parsing.nmapParsing import *
from parsing.whoisParsing import *
from subprocessUtils.subprocess import *

def ipAi(ip):
    print("[+] Nous avons puis joindre l'hôte")

    #faire un whois
    stdoutWhois, stderrWhois = asyncio.run(doWhois(ip))
    print(f"[+] Recherche enregistrement DNS de {ip} terminé")
    print(stdoutWhois)
        
    #faire un scan de ports
    stdoutNmap, stderrNmap = asyncio.run(doNmap(ip))
    print(f"[+] Scan nmap de {ip}  terminé")
    print(stdoutNmap)


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
            pass

        