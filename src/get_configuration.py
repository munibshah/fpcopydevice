from firerest76 import FMC
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
        create_backup()
        clear_output_folder("output")

        #Initialize the FMC object and get the container ID for ftdname
        fmc = FMC(hostname=host, username=username, password=password, domain='Global')
        Device = fmc.device.devicerecord.get(name=ftdname)
        containerID = Device.get('id')
        print(containerID)

        #Create Interface Directory
        Intffolderpath =f"output/Interfaces"
        os.makedirs(Intffolderpath, exist_ok=True)

        #Extract fields and save inside Interfaces folder as json and yaml
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Physical interfaces saved in {Intffolderpath}")
        get_phyintf(fmc,containerID,folderpath="output/Interfaces")

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Etherchannel interfaces saved in {Intffolderpath}")
        get_etherintf(fmc,containerID,folderpath="output/Interfaces")

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Sub-interfaces interfaces saved in {Intffolderpath}")
        get_subintf(fmc,containerID,folderpath="output/Interfaces")
        
        #Get VirtualRouters and save it to the output folder 
        VRfolderpath="output"
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Virtual Routing Configuration saved in {VRfolderpath}")
        virtualrouters = get_vr(fmc,containerID,folderpath=VRfolderpath)


        #vr_list =[]
        for vr in virtualrouters:
            

            #Main directory for all VRFs 
            directory =f"output/VirtualRouters/{vr["name"]}"
            os.makedirs(directory, exist_ok=True)
            
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] VRF IPv4 Static Routes saved in {directory}")
            get_vr_ipv4staticroutes(fmc,containerID,vr["id"],folderpath=directory)

            
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] VRF BGP Routes saved in {directory}")
            get_vr_bgproutes(fmc,containerID,vr["id"],folderpath=directory)

            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] VRF ECMP configuration saved in {directory}")
            get_vr_ecmpzones(fmc,containerID,vr["id"],folderpath=directory)

    else:
        print("\nExiting program..")
if __name__ == "__main__":
    main()