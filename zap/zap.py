#!/usr/bin/env python
# A basic ZAP Python API example which spiders and scans a target URL

import time
from pprint import pprint
from zapv2 import ZAPv2



def zap(ip, webProtocol, apiParam=None):
    target = f"{webProtocol}://{ip}"
    apikey = apiParam
    zap = ZAPv2(apikey=apikey)

    print(f"[+] Accessing target: {target}")
    zap.urlopen(target)
    time.sleep(2)

    print("[+] Disabling all scanners...")
    zap.ascan.disable_all_scanners()

    print("[+] Enabling selected scanners: XSS (40012), SQLi (40014), etc.")
    zap.ascan.enable_scanners("40012,40014,40018")

    print(f"[+] Starting active scan on: {target}")
    scanid = zap.ascan.scan(target, recurse=False)

    while int(zap.ascan.status(scanid)) < 100:
        print(f"    [+] Scan progress: {zap.ascan.status(scanid)}%")
        time.sleep(5)

    print("[+] Scan completed")
    #print("[+] Hosts found:", ", ".join(zap.core.hosts))
    print("[+] Alerts:")
    pprint(zap.core.alerts())  # affichage seulement

    return zap.core.alerts() 


if __name__ == "__main__":
    print(zap("127.0.0.1", "http", "a3vb0hvphqbu7ruhvpql9l5ufm"))