import asyncio

#mes packages
from parsing.whoisParsing import *
from parsing.nmapParsing import *
from parsing.nucleiParsing import *




async def runCommand(cmd, name):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()
    print(f'[{name}] {cmd!r} exited with {proc.returncode}')
    
    #ici j'ai retourné stdout et err pour les utiliser dans les autres fonctions
    return stdout.decode(), stderr.decode()


"""async def doPing(host):
    cmd = f"ping -c 5  {host}"
    print("[+] Nous tentons  de joindre l'hôte")
    stdout, stderr = await runCommand(cmd, "ping")

    return stdout, stderr


async def doWhois(host):
    cmd = f"whois {host}"
    print(f"[+] Recherche enregistrement DNS derriere {host}")
    
    stdout, stderr = await runCommand(cmd, "whois")

    if stdout:
        stdout = whoisParsing(stdout)

    return stdout, stderr"""


async def doNmap(host):
    cmd = f"nmap  -sV -O --script=vuln {host} -oX {host}Nmap.xml"
    print(f"[+] Scan de ports et versions des services {host}")
    
    stdout, stderr = await runCommand(cmd, "nmap")
    if stdout:
        stdout = nmapParsing(f"{host}Nmap.xml")

    return stdout, stderr


"""async def nuclei(host):
    cmd = f"nuclei -target {host} -output {host}Nuclei.txt"
    print(f"Vulnerability scan on {host} with nuclei")

    stdout, stderr = await runCommand(cmd, "nuclei")
    if stdout:
        stdout = nucleiParsing(f"{host}Nuclei.txt")
    return stdout, stderr"""

