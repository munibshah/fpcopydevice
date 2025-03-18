from fireREST import FMC
from config.create import *
from dotenv import load_dotenv # type: ignore
import argparse
from src.get_configuration import *

def initialize_vr_get_id(vrfolderpath="output"):
    virtualrouters = get_vr(fmc,containerID,folderpath=vrfolderpath)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Virtual Routing Configuration saved in {vrfolderpath}")

    for vr in virtualrouters:
            #Main directory for all VRFs 
            directory =f"output/VirtualRouters/{vr["name"]}"
            os.makedirs(directory, exist_ok=True)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] New VRF ID saved in {directory}")
            get_vrid(directory,vr['name'])

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

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Virtual Routing Configuration saved in {vrfolderpath}")
    virtualrouters = get_vr(fmc,containerID,folderpath=vrfolderpath)

    for vr in virtualrouters:
            #Main directory for all VRFs 
            foldername =f"output/VirtualRouters/{vr["name"]}"
            os.makedirs(foldername, exist_ok=True)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] New VRF ID saved in {foldername}")
            get_vrid(foldername)
    return(fmc,containerID,vrfolderpath,vrdirectory)