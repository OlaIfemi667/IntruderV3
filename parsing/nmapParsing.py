import xml.etree.ElementTree as ET
import json
import re

from typing import List, Tuple, Any
import ast


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
    #       "ports": [{"protocol": "TCP", "port": "80", "service": "HTTP"(or unknown if unknown), "product": "xxxx", "version": "2.1.0"}, "edb-ids": [list of EDB-ID]],
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
            if service is not None:
                service_name = service.attrib.get('name', 'unknown')
                product = service.attrib.get('product', '')
                version = service.attrib.get('version', '')
            else:
                service_name = 'unknown'
                product = ''
                version = ''
            
            port_info = {
                'protocol': port.attrib['protocol'],
                'port': int(port.attrib['portid']),
                'service': service_name,
                'product': product,
                'version': version,
                'edb_ids': []
            }
            portID = int(port.attrib['portid'])

            for script in port.findall(".//script"):
                for table in script.findall(".//table"):
                    for elem in table.findall(".//elem"):
                        if elem.text and is_edb_format(elem.text):
                            edb_id = elem.text.split("EDB-ID:")[1].strip()
                            print(f"> EDB-ID trouvé : {edb_id} sur le port {portID}")
                            port_info['edb_ids'].append(edb_id)

            if port_info['edb_ids'].len() != 0:
                host_info['ports'].append(port_info)


           

        osmatch = host.find('.//osmatch')
        if osmatch is not None:
            host_info['os'] = {
                'name': osmatch.attrib['name'],
                'accuracy': int(osmatch.attrib['accuracy'])
            }

        results.append(host_info)

    return json.dumps(results, indent=4)







def convertTuples(input_list: List[Tuple[Any, Any, str, Any]]) -> List[Tuple[Any, Any, dict, Any]]:
    #pour attribuer les types normal a mes output de la db
    result = []
    for item in input_list:
        raw_value = item[2]
        parsed_dict = {}

        if isinstance(raw_value, str):
            try:
                parsed_dict = json.loads(raw_value)  # Essaye JSON d'abord
            except json.JSONDecodeError:
                try:
                    parsed_dict = ast.literal_eval(raw_value)  # Fallback : Python dict
                    if not isinstance(parsed_dict, dict):
                        raise ValueError("Not a dict")
                except (ValueError, SyntaxError):
                    print(f"Warning: Cannot parse {raw_value}, using empty dict.")
        elif isinstance(raw_value, dict):
            parsed_dict = raw_value
        else:
            print(f"Warning: Unsupported format {type(raw_value)}")

        result.append((item[0], item[1], parsed_dict, item[3]))
    return result


if __name__  == "__main__":    
    print(nmapParsing("172.16.93.128Nmap.xml"))