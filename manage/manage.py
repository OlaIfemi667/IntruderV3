from database.database import * 

def manager():
    a = choiceProcess()
    

def choiceProcess():
    choice = input("> Enter your choice: ")
    while True:
        if choice.strip() in ["1", "2", "3", "4", "5"]:
            askchoice(choice.strip())
            return choiceProcess()
        else:
            print("Invalid choice. Please try again.")
            return choiceProcess()
    
def askchoice(choice):
    if choice == "1":
        print("Listing all scans...")
        scans = getAllScans()
        if scans:
            for scan in scans:
                print(f"Scan Name: {scan['scanName']}, Create by: {getanUsername(scan['userId'])}")
        else:
            print("No scans found.")
    elif choice == "2":
        print("Exporting a scan report...")
        # Call the function to export a scan report
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