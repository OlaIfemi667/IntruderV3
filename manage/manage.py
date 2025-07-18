from database.database import * 
from asciart.asciiart import *

def manager():
    a = choiceProcess()
    
def choiceProcess():
    print(INTRUDER_MANAGER_QUESTIONS)
    choice = input("\n> Enter your choice: ")
    while True:
        if choice.strip() in ["1", "2", "3", "4", "5"]:
            askchoice(choice.strip())
            return choiceProcess()
        else:
            print("Invalid choice. Please try again.")
            return choiceProcess()
    
def askchoice(choice):
    if choice == "1":
        print("\nListing all scans...\n")
        scans = getAllScans()
        if scans:
            for scan in scans:
                print(f"Scan Name: {scan['scanName']}, Create by: {getanUsername(scan['userId'])}")
        else:
            print("No scans found.")
    elif choice == "2":
        print("\nSelect a scan by its ID to export its details: \n")
        scans = getAllScans()
        if not scans:
            print("No scans available to export.")
            return
        for scan in scans:
            print(f"Scan ID: {scan['id']}, Scan Name: {scan['scanName']}, Created by: {getanUsername(scan['userId'])}")

        scanID = input("\nEnter the scan ID to export its details: \n")
        scanID = scanID.strip()

        if not scanID.isdigit():
            print("Invalid scan ID. Please enter a numeric value.")
            return choiceProcess()
        
        choseID = [s["id"] for s in scans if s["id"] == int(scanID)]
        
        if len(choseID) == 1:
            print(f"Exporting details for scan ID {scanID}...")

            # MAintenant j'exporte vraiment le scan

        else:
            print(f"No scan found with ID {scanID}. Please try again.")
            return choiceProcess()

    elif choice == "3":
        print("Setting up ZAP API key...")
        # Call the function to set up ZAP API key
    elif choice == "4":
        print("Setting up Groq API key...")
        # Call the function to set up Groq API key
    elif choice == "5":
        print("Exiting the management console. Goodbye!")
        exit(0)
    else:
        print("Invalid choice. Please try again.")