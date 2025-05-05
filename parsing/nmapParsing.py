import xml.etree.ElementTree as ET
import json

def nmapParsing(fichierXml):

    #charger le fichier xml output de nmap
    tree = ET.parse(fichierXml)
    root = tree.getroot()
    results = []

    #récuperer les informations (ip, ports , versions et type os) pour chaques champs hosts dans le XML
    for host in root.findall('host'):
        host_info = {}
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
                'version': service.attrib.get('version', '')
            }
            host_info['ports'].append(port_info)

        osmatch = host.find('.//osmatch')
        if osmatch is not None:
            host_info['os'] = {
                'name': osmatch.attrib['name'],
                'accuracy': int(osmatch.attrib['accuracy'])
            }

        results.append(host_info)

    return json.dumps(results, indent=4)

