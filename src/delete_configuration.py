from fireREST import FMC
import json
from config.delete import *
from utils.create_backup import create_backup
from dotenv import load_dotenv # type: ignore
import argparse
import argparse

    


# Read YAML file

def main():
    load_dotenv(dotenv_path=".env")
    host = os.getenv("HOST")
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    ftdname = os.getenv("FTDNAME")

    #Initialize the FMC object and get the container ID for ftdname
    
    fmc = FMC(hostname=host, username=username, password=password, domain='Global')
    Device = fmc.device.devicerecord.get(name=ftdname)
    containerID = Device.get('id')
    folderpath ="output"
    
    create_backup()
    print("Deleting all Subinterfaces and related configuration")
    delete_subintf(fmc,containerID,folderpath)
    print(host)
    print("Deleting all VRs and related configuration")
    delete_vr(fmc,containerID,folderpath)
    
    

if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument('--function',choices=['detele_subintf','delete_subintf','delete_etherintf','delete_vr','delete_vr_ipv4staticroutes','delete_vr_ecmpzones','delete_vr_bgp','all'],help='Options to choose from:')
    args = parse.parse_args()
    
    load_dotenv(dotenv_path=".env")
    host = os.getenv("HOST")
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    ftdname = os.getenv("FTDNAME")

    #Initialize the FMC object and get the container ID for ftdname
    
    fmc = FMC(hostname=host, username=username, password=password, domain='Global')
    Device = fmc.device.devicerecord.get(name=ftdname)
    containerID = Device.get('id')
    folderpath ="output"
    

    if args.function == 'delete_vr':
        create_backup()
        print("Deleting all VRs and related configuration")
        delete_vr(fmc,containerID,folderpath)

    
    elif args.function == 'delete_subintf':
        create_backup()
        print("Deleting all Subinterfaces and related configuration")
        delete_subintf(fmc,containerID,folderpath)
        
    elif args.function == 'all':
        main()
