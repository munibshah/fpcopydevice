from fireREST import FMC
from config.create import *
from .get_configuration import *
from dotenv import load_dotenv # type: ignore
import argparse
from utils.initialize import *

# Read YAML file

def main():
    
    fmc,containerID,folderpath,vrdirectory=initialize_fmc_object()
    
    
    #Get created ipv4staticroutes by iterating over every folder in the folder VR. vr.json is used for the ID 
    create_vr_ipv4staticroutes(fmc,containerID,vrdirectory)
    
    create_vr_ecmpzones(fmc,containerID,vrdirectory)
    
    create_vr_bgp(fmc,containerID,vrdirectory)
    
    print("Run get_configuration to update json data for delete to work..")

if __name__ == "__main__":

    parse = argparse.ArgumentParser()
    parse.add_argument('--function',choices=['create_phyintf','create_subintf','create_etherintf','create_vr','create_vr_ipv4staticroutes','create_vr_ecmpzones','create_vr_bgp','all'],help='Options to choose from:')
    args = parse.parse_args()

    if args.function == 'create_phyintf':
        fmc,containerID,folderpath,vrdirectory=initialize_fmc_object()
        print(containerID)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Creating Physical Interfaces in {folderpath}")
        create_phyintf(fmc,containerID,"output/Interfaces")
    
    if args.function == 'create_etherintf':
        fmc,containerID,folderpath,vrdirectory=initialize_fmc_object()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Creating Etherchannel Interfaces in {folderpath}")
        create_etherintf(fmc,containerID,"output/Interfaces")

    if args.function == 'create_subintf':
        fmc,containerID,folderpath,vrdirectory=initialize_fmc_object()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Creating Subinterfaces Interfaces in {folderpath}")
        create_subintf(fmc,containerID,"output/Interfaces")

    if args.function == 'create_vr':
        fmc,containerID,folderpath,vrdirectory=initialize_fmc_object()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Creating VR from {vrdirectory}/vr.json")
        create_vr(fmc,containerID,folderpath)

    elif args.function == 'create_vr_ipv4staticroutes':
        fmc,containerID,folderpath,vrdirectory=initialize_fmc_object_with_vr()
        initialize_vr_get_id(fmc,containerID)
        create_vr_ipv4staticroutes(fmc,containerID,vrdirectory)

    elif args.function == 'create_vr_ecmpzones':
        fmc,containerID,folderpath,vrdirectory=initialize_fmc_object_with_vr()
        initialize_vr_get_id(fmc,containerID)
        create_vr_ecmpzones(fmc,containerID,vrdirectory)

    elif args.function == 'create_vr_bgp':
        fmc,containerID,folderpath,vrdirectory=initialize_fmc_object_with_vr()
        initialize_vr_get_id(fmc,containerID)
        create_vr_bgp(fmc,containerID,vrdirectory)
    
    elif args.function == 'all':
         main()