def whoisParsing(output: str) -> dict:

    #logique simple pour parser mes whois pour ne pas avoir a dealer avec les output verbeux de whois
    info = {}

    for line in output.splitlines():
        line = line.strip()
        if line.lower().startswith("domain name:"):
            info["domain"] = line.split(":")[1].strip()
        elif line.lower().startswith("creation date:"):
            info["creation_date"] = line.split(":")[1].strip()
        elif line.lower().startswith("registry expiry date:") or line.lower().startswith("expiration date:"):
            info["expiration_date"] = line.split(":")[1].strip()
        elif line.lower().startswith("registrar:"):
            info["registrar"] = line.split(":")[1].strip()
        elif line.lower().startswith("name server:"):
            info.setdefault("name_servers", []).append(line.split(":")[1].strip())
        elif line.lower().startswith("domain status:"):
            info.setdefault("status", []).append(line.split(":")[1].strip())

    #ce sont ces champs qui m'interresse si {} est retourne ça veut juste que ce whois ne contient pas d'information qui m'interresse
    return info
