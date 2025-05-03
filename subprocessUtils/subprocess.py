import asyncio
from urllib.parse import urlparse

async def runCommand(cmd, type):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()
    a = ""
    print(f'[{cmd!r} exited with {proc.returncode}]')
    
    #ici j'ai retourné stdout et err pour les utiliser dans les autres fonctions
    return stdout.decode(), stderr.decode()
    


def is_valid_url(url: str) -> bool:
    parsed = urlparse(url)
    return all([parsed.scheme in ('http', 'https'), parsed.netloc])



async def doPing(host):
    cmd = f"ping -c 5  {host}"
    print("[+] Nous tentons  de joindre l'hôte")
    stdout, stderr = await runCommand(cmd, "ping")

    return stdout, stderr


async def doWhois(host):
    cmd = f"whois {host}"
    print(f"[+] Recherche enregistrement DNS derriere {host}")
    
    stdout, stderr = await runCommand(cmd, "whois")
    

    return stdout, stderr


async def doNmap(host):
    cmd = f"nmap -sV -O {host}"
    print(f"[+] Scan de ports et versions des services {host}")
    
    stdout, stderr = await runCommand(cmd, "nmap")

    return stdout, stderr
