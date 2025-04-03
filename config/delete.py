import os
import shutil
import json
from datetime import datetime

def create_backup(folder_name='output'):
    if not os.path.exists(folder_name):
        print(f"Folder '{folder_name}' does not exist.")
        return
    
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"backup_{timestamp}.zip"
    
    shutil.make_archive(backup_name.replace('.zip', ''), 'zip', folder_name)
    
    print(f"Backup created: {backup_name}")

def clear_output_folder(output_dir="output"):
    """
    Removes all files and subfolders inside the given 'output_dir', but leaves
    the directory itself intact. If you want to remove only files while
    keeping subfolders, remove the 'shutil.rmtree(file_path)' part.

    :param output_dir: (str) Path to the folder to clear. Defaults to 'output'.
    """
    if os.path.exists(output_dir):
        for filename in os.listdir(output_dir):
            file_path = os.path.join(output_dir, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    else:
        print(f"The folder '{output_dir}' does not exist.")

def delete_vr(fmc,containerID,folderpath):
    vrfilepath = os.path.join(folderpath, "vr.json")
    with open(vrfilepath, mode="r") as file:
        data = json.load(file)
    for vrf in data:
        vrf_id = vrf["id"]
        vrf_name = vrf["name"]
        if vrf_name.lower() != "global":
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Deleting {vrf_name} with uuid {vrf_id}")
            fmc.device.devicerecord.routing.virtualrouter.delete(uuid=vrf_id,container_uuid=containerID)

def delete_subintf(fmc,containerID,folderpath):
    with open("output/Interfaces/subintf.json", mode="r") as file:
        data = json.load(file)
    for intf in data:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Deleting Interface with name {intf["ifname"]}")
        fmc.device.devicerecord.subinterface.delete(uuid=intf["id"],container_uuid=containerID)

        
