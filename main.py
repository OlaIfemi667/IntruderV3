import typer
import shutil
from typing import Annotated

#my packages
from subprocessUtils.subprocess import * #for  subprocess handling
from parsing.whoisParsing import * #to parse whois output
from parsing.nmapParsing import * #to parse nmap
from commandsFunctions.ipFunction import * #logique when only ip is provide
from database.database import * #for db SQLite operations
from asciart.asciiart import *
from manage.manage import manager


from app.main import app as web_app


def checkRequiredSysBin():
    required_bins = ["nmap", "zaproxy"]
    all_present = True

    for bin_name in required_bins:
        if not shutil.which(bin_name):
            typer.echo(f"Error: {bin_name} is not installed or not found in PATH.")
            all_present = False
        else:
            typer.echo(f"[+] {bin_name} is installed.")

    return all_present


init_db() # this line is so obvious :)
app = typer.Typer()


# pour exécuter un scan , may delete i soon
@app.command()
def scan(name: Annotated[str, typer.Argument(help="Scan name")],ip: Annotated[str, typer.Argument(help="IP address to scan")], domain: Annotated[str, typer.Option(help="domain to scan")] = "None"):
    print(f"Scan name: {name}")
    
    #stdoutNuc, stderrNuc = asyncio.run(nuclei(ip))
    if checkScanExists(name) == True:
        print(f"[!] Scan with name {name} already exists. Please choose a different name.")
        return
    if ip and domain == "None":
        #faire un ping
        stdoutPing, stderrPing = asyncio.run(doPing(ip))

        #si ping réussi
        if stdoutPing:
            asyncio.run(ipAi(ip, name, domain))

@app.command()
def web():
    # Pour lancer l'application web
    typer.echo("Starting web application...")
    web_app.run(debug=True)



@app.command()
def manage():
    # la commde pour gerer l'outil
    print(INTRUDER_MANAGER)
    manager()



if __name__ ==  "__main__":
    if  checkRequiredSysBin() == True:
        app()
    else:
        typer.echo("Required binaries are not installed. Please install them and try again.")
