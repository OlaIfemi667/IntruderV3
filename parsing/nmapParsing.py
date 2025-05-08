import xml.etree.ElementTree as ET
import json

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
    #       "ports": [{"protocol": "TCP", "port": "80", "service": "HTTP"(or unknown if unknown), "product": "xxxx", "version": "2.1.0"}],
    #       "os": {"name": "linux"}
    #   }
    #]
    for host in root.findall('host'):
        host_info = {}
        host_info['ip'] = host.find('address').attrib['addr']
        host_info['ports'] = []
        host_info['os'] = None
        host_info['cve'] = []

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
            portID = int(port.attrib['portid'])

            #Parsing this shit was so fucking insane for me

            #i figure it out this is basiccally the layout ou host_info["cve"]

            #[
            #   [portID, id(scriptID), [{"id_table": [tableElement],..,...,}],
            #   [portID, id(scriptID), [{"id_table": [tableElement],..,...,}],    
            #   [portID, id(scriptID), [{"id_table": [tableElement],..,...,}],
            #   ..
            #   ..
            #   ]
            #]

            #
            #
            # So ti is basically a list of script information-list
            for script in port.findall("script"):
                
                structScript = []
                structScript.append(portID)
                #structScript.append(script.get("output"))
                structScript.append(script.get("id"))
                print(f"IDDDDDD: {script.get("id")}")

                tableAll = {}
                tableCount = 0
                for table in script.findall("table"):
                    
                    tableElement = []
                    tableElementKey = str(tableCount)
                    for element in table.findall("elem"):
                        tableElement.append({element.get("key"): element.text})
                    
                    tableAll[tableElementKey] = tableElement
                    tableCount+=1
                if tableAll != {}  and tableAll.get("0"):
                    structScript.append(tableAll)
                    host_info["cve"].append(structScript)

                

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