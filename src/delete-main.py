from fireREST import FMC
import json
from config.cleanup import *
from utils.create_backup import create_backup

    


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
    folderpath ="output"
    create_backup()
    delete_vr(fmc,containerID,folderpath)

if __name__ == "__main__":
    main()
