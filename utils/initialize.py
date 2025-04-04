from firerest76 import FMC
from config.create import *
from dotenv import load_dotenv # type: ignore
import argparse
from src.get_configuration import *
from config.write import *

def initialize_vr_get_id(fmc,containerID,vrfolderpath="output"):
    #Fetches from FMC and stores in vr.json
    virtualrouters = get_vr(fmc,containerID,folderpath=vrfolderpath)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Virtual Routing Configuration saved in {vrfolderpath}")

    for vr in virtualrouters:
            #Main directory for all VRFs 
            vrfoldername =f"output/VirtualRouters/{vr["name"]}"
            os.makedirs(vrfoldername, exist_ok=True)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] New VRF ID saved in {vrfoldername}")
            get_vrid(vrfoldername)

def initialize_fmc_object():
    load_dotenv(dotenv_path=".env")
    host = os.getenv("HOST")
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    ftdname = os.getenv("FTDNAME")

    #Initialize the FMC object and get the container ID for ftdname

    fmc = FMC(hostname=host, username=username, password=password, domain='Global')
    Device = fmc.device.devicerecord.get(name=ftdname)
    containerID = Device.get('id')
    vrfolderpath = "output"
    vrdirectory = "output/VirtualRouters"

    return(fmc,containerID,vrfolderpath,vrdirectory)

def initialize_fmc_object_with_vr():
      
        load_dotenv(dotenv_path=".env")
        host = os.getenv("HOST")
        username = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")
        ftdname = os.getenv("FTDNAME")

    #Initialize the FMC object and get the container ID for ftdname

        fmc = FMC(hostname=host, username=username, password=password, domain='Global')
        Device = fmc.device.devicerecord.get(name=ftdname)
        containerID = Device.get('id')
        vrfolderpath = "output"
        vrdirectory = "output/VirtualRouters"
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Virtual Routing Configuration saved in {vrfolderpath}")
        
        #Fetches from FMC and stores in vr.json
        virtualrouters = get_vr(fmc,containerID,folderpath=vrfolderpath) 
        for vr in virtualrouters:
                vrfoldername =f"output/VirtualRouters/{vr["name"]}"
                os.makedirs(vrfoldername, exist_ok=True)
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] New VRF ID saved in {vrfoldername}")
                write_vr_id(vr["id"],vrfoldername) # Write vd["id"] to the vrid.json in each VR folder 
        return (fmc,containerID,vrfolderpath,vrdirectory)