import os
import json
from utils.utility import *
from datetime import datetime
import sys


def write_vr_id(vr_id,folderpath="output/VirtualRouters"):

    id_obj = {
            "id": vr_id
        }
    vr_string = json.dumps(id_obj,indent=2) #To save VR_ID in the VirtualRouters folder 
    vridoutput = os.path.join(folderpath, "vrid.json")
    with open(vridoutput, "w") as f:
            f.write(vr_string)


    