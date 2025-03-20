import os
import json
from utils.utility import *
from datetime import datetime
import sys


def write_vr_id(vr_id, folderpath="output/VirtualRouters"):
    #VR = fmc.device.devicerecord.routing.virtualrouter.get(container_uuid=containerID,child_container_uuid=vr_id)

    #print(ecmpzone)
    # Build the minimal dictionary with the keys you want in your YAML
    id_obj = {
            "id": vr_id
        }
    vr_string = json.dumps(id_obj,indent=2) #To save VR_ID in the folder 
    vridoutput = os.path.join(folderpath, "vrid.json")
    with open(vridoutput, "w") as f:
            f.write(vr_string)
            print("wrote to")
            print(vridoutput)


    