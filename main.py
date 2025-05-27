import typer
from typing import Annotated

#my packages
from subprocessUtils.subprocess import * #for  subprocess handling
from parsing.whoisParsing import * #to parse whois output
from parsing.nmapParsing import * #to parse nmap
from commandsFunctions.ipFunction import * #logique when only ip is provide
from database.database import * #for db SQLite operations


init_db() # this line is so obvious
app = typer.Typer()



@app.command()
def scan(name: Annotated[str, typer.Argument(help="Scan name")],ip: Annotated[str, typer.Argument(help="IP address to scan")], domain: Annotated[str, typer.Option(help="domain to scan")] = "None"):
    print(f"Scan name: {name}")
    addScan(name, ip, domain)
    #stdoutNuc, stderrNuc = asyncio.run(nuclei(ip))
    if ip and domain == "None":
        #faire un ping
        stdoutPing, stderrPing = asyncio.run(doPing(ip))

        #si ping réussi
        if stdoutPing:
            asyncio.run(ipAi(ip, name))


    elif ip and domain != "None":
        print("ls")


@app.command()
def report( scanName: Annotated[str, typer.Argument(help="domains to scan to scan OS")]):
    print(f"report {scanName}")

if __name__ ==  "__main__":
    app()