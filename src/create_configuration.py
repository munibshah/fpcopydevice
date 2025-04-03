from config.create import *
from .get_configuration import *
from dotenv import load_dotenv # type: ignore
import argparse
from utils.initialize import *
from config.update import update_vr_with_intfid



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

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Sub-interfaces interfaces saved in output/Interfaces")
        get_subintf(fmc,containerID,"output/Interfaces")

        vr_name_id_map = get_name_id_mapping(fmc,containerID,childID="subintf") #get new id and name from the fmc using subintf.get (live get)
        update_vr_with_intfid(vr_name_id_map) #update the VR with Interfaces which have the same ifname in name-map. This needs to be repeated for every interface type.

    if args.function == 'create_vr':
        fmc,containerID,folderpath,vrdirectory=initialize_fmc_object()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Creating VR from {vrdirectory}/vr.json")
        create_vr(fmc,containerID,folderpath="output")

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Virtual Routing Configuration saved in output/vr.json")
        virtualrouters = get_vr(fmc,containerID,folderpath="output") #Get and store new VR configuration in output/vr.json
        for vr in virtualrouters:
            write_vr_id(vr["id"],vr["name"],"output/VirtualRouters") #write vrid per folder 


    elif args.function == 'create_vr_ipv4staticroutes':
        #Initialize fmc object, getes VRs from FMC and stores in vr.json, writes from geted list in {VRfolder}/vr.json
        fmc,containerID,folderpath,vrdirectory=initialize_fmc_object_with_vr() 
        #Read the vrid.json file and return the id.
        #initialize_vr_get_id(fmc,containerID)
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