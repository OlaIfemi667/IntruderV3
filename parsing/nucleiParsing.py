import re
from collections import defaultdict

def nucleiParsing(file_path):
    port_vulns = defaultdict(list)
    severity_order = {'info': 0, 'low': 1, 'medium': 2, 'high': 3, 'critical': 4}

    with open(file_path, 'r') as f:
        for line in f:
            match = re.search(r'\[(.*?)\] \[(.*?)\] \[(.*?)\] (.*?)$', line)
            if match:
                name, protocol, severity, target = match.groups()
                severity = severity.lower()
                #Récuperer le port ici
                port_match = re.search(r':(\d+)', target)
                port = port_match.group(1) if port_match else 'unknown'

                if severity in ('high', 'critical'):
                    port_vulns[port].append((severity, line.strip()))

    result = {}
    for port, vulns in port_vulns.items():
       #on récuperer la ligne ayant la plus grosse sévérité pour chaque
        highest = max(vulns, key=lambda v: severity_order[v[0]])
        result[port] = highest[1]

    return 


if __name__ == "__main__":
    file_path = 'vulns.txt' 
    high_vulns = extract_high_vulns_per_port(file_path)
    
    print(len(high_vulns))
