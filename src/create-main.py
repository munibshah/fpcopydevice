from fireREST import FMC
from config.create import *
from .get_main import *


# Read YAML file

def main():
    host = ""
    username = ""
    password = ""
    ftdname = ""  

    #Initialize the FMC object and get the container ID for ftdname

    fmc = FMC(hostname=host, username=username, password=password, domain='Global')
    Device = fmc.device.devicerecord.get(name=ftdname)
    containerID = Device.get('id')
    folderpath = "output"
    vrdirectory = "output/VirtualRouters"

    #Creates VR by reading output/vr.json
    #create_vr(fmc,containerID,folderpath)
    VRfolderpath="output"
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Creating VR in {VRfolderpath}")
    create_vr(fmc,containerID,folderpath)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Virtual Routing Configuration saved in {VRfolderpath}")
    virtualrouters = vr_yaml(fmc,containerID,folderpath=VRfolderpath)

    for vr in virtualrouters:
            #Main directory for all VRFs 
            directory =f"output/VirtualRouters/{vr["name"]}"
            os.makedirs(directory, exist_ok=True)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] New VRF ID saved in {directory}")
            vr_bgp_routes_yaml(fmc,containerID,vr["id"],folderpath=directory,vridonly=True)
    
    #Get created ipv4staticroutes by iterating over every folder in the folder VR. vr.json is used for the ID 
    create_vr_ipv4staticroutes(fmc,containerID,vrdirectory)
    
    create_vr_ecmpzones(fmc,containerID,vrdirectory)
    
    create_vr_bgp(fmc,containerID,vrdirectory)
    
    print("Run get_main to update json data for delete to work..")

if __name__ == "__main__":
    main()
