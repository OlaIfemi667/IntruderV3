import typer
from subprocessUtils.subprocess import *
from parsing.whoisParsing import *

from typing import Annotated

app = typer.Typer()



@app.command()
def scan(name: Annotated[str, typer.Argument(help="Scan name")],ip: Annotated[str, typer.Argument(help="IP address to scan")], domain: Annotated[str, typer.Option(help="domain to scan")] = "None"):
    print(f"Scan name: {name}")
    if ip and domain == "None":
        #faire un ping
        stdoutPing, stderrPing = asyncio.run(doPing(ip))

        #si ping réussi
        if stdoutPing:
            print("[+] Nous avons puis joindre l'hôte")

            #faire un whois
            stdoutWhois, stderrWhois = asyncio.run(doWhois(ip))
            print(f"[+] Recherche enregistrement DNS de {ip} terminé")
            print(stdoutWhois)
        

            #faire un scan de ports
            stdoutNmap, stderrNmap = asyncio.run(doNmap(ip))
            print(f"[+] Scan nmap de {ip}  terminé")
            print(stdoutNmap)


            #for each service search exploits
            #if here is a wb server check to 10 owasp


    elif ip and domain != "None":
        print("ls")


@app.command()
def report( scanName: Annotated[str, typer.Argument(help="domains to scan to scan OS")]):
    print(f"report {scanName}")

if __name__ ==  "__main__":
    app()