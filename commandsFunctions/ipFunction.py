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
    #       "ports": [{"protocol": "TCP", "port": "80", "service": "HTTP"(or unknown if unknown), "product": "xxxx", "version": "2.1.0"}],
    #       "os": {"name": "linux"}
    #   }
    #]

    for port in nmapOutput["ports"]:
        searchSploit(f"{port["service"]} {port["version"]}")
        