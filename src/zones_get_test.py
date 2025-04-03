from fireREST import FMC
import os 
import argparse
from datetime import datetime
from config.get import *
from utils.create_backup import create_backup
from config.delete import clear_output_folder
from dotenv import load_dotenv # type: ignore


def main():
    load_dotenv(dotenv_path=".env", override=True)
    host = os.getenv("HOST")
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    ftdname = os.getenv("FTDNAME")
    print(host)
    
    user_input = input("This operation will overwrite all files in the output folder. Do you wish to proceed [Y]: ")
    if user_input.upper() == "Y":
        # create_backup()
        # clear_output_folder("output")

        #Initialize the FMC object and get the container ID for ftdname
        fmc = FMC(hostname=host, username=username, password=password, domain='Global')
        Device = fmc.device.devicerecord.get(name=ftdname)
        containerID = Device.get('id')
        print(containerID)

        #Create Interface Directory
        SecurityZones =f"output/SecurityZones"
        os.makedirs(SecurityZones, exist_ok=True)
        

    else:
        print("\nExiting program..")
if __name__ == "__main__":
    main()