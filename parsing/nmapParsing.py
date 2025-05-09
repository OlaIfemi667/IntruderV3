import xml.etree.ElementTree as ET
import json
import re



def is_edb_format(value):
    pattern = r"^EDB-ID:\d+$"
    return bool(re.match(pattern, value))



def nmapParsing(fichierXml):

    #charger le fichier xml output de nmap
    tree = ET.parse(fichierXml)
    root = tree.getroot()
    results = []

    #récuperer les informations (ip, ports , versions et type os) pour chaques champs hosts dans le XML
    #so the format is like this
    #[
    #   {
    #       "ip": "aRandomIPaddress",
    #       "ports": [{"protocol": "TCP", "port": "80", "service": "HTTP"(or unknown if unknown), "product": "xxxx", "version": "2.1.0"}, "edb-ids": ]],
    #       "os": {"name": "linux"}
    #   }
    #]
    host_info = {}
    for host in root.findall('host'):
        
        host_info['ip'] = host.find('address').attrib['addr']
        host_info['ports'] = []
        host_info['os'] = None
        

        for port in host.findall('.//port'):
            if port.find('state').attrib['state'] != 'open':
                continue

            service = port.find('service')
            port_info = {
                'protocol': port.attrib['protocol'],
                'port': int(port.attrib['portid']),
                'service': service.attrib.get('name', 'unknown'),
                'product': service.attrib.get('product', ''),
                'version': service.attrib.get('version', ''),
                'edb_ids': [] 
            }
            host_info['ports'].append(port_info)
            portID = int(port.attrib['portid'])

            host_info['cve'] = []
            for script in port.findall(".//script"):
                for table in script.findall(".//table"):
                    for elem in table.findall(".//elem"):
                        if elem.text and is_edb_format(elem.text):
                            edb_id = elem.text.split("EDB-ID:")[1].strip()
                            print(f"➡️ EDB-ID trouvé : {edb_id} sur le port {portID}")
                            port_info['edb_ids'].append(edb_id)

            host_info['ports'].append(port_info)

           

        osmatch = host.find('.//osmatch')
        if osmatch is not None:
            host_info['os'] = {
                'name': osmatch.attrib['name'],
                'accuracy': int(osmatch.attrib['accuracy'])
            }

        results.append(host_info)

    return json.dumps(results, indent=4)

if __name__  == "__main__":    
    print(nmapParsing("172.16.93.128Nmap.xml"))