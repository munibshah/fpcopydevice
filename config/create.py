import os
import json
from utils.utility import *
from datetime import datetime
from config.write import *
from config.fetch import *

def create_subintf(fmc,containerID,folderpath="output/Interfaces"):
    phyintfvrfilepath = os.path.join(folderpath, "subintf.json")
    with open(phyintfvrfilepath, mode="r") as file:
        data = json.load(file)
    for intf in data:
        print(intf)
        fmc.device.devicerecord.subinterface.create(intf,container_uuid=containerID)

def create_etherintf(fmc,containerID,folderpath="output/Interfaces"):
    phyintfvrfilepath = os.path.join(folderpath, "etherintf.json")
    with open(phyintfvrfilepath, mode="r") as file:
        data = json.load(file)
    for intf in data:
        print(intf)
        fmc.device.devicerecord.etherchannelinterface.create(intf,container_uuid=containerID)

def create_phyintf(fmc,containerID,folderpath):
    phyintfvrfilepath = os.path.join(folderpath, "phyintf.json")
    with open(phyintfvrfilepath, mode="r") as file:
        data = json.load(file)
    for intf in data:
        print(intf)
        fmc.device.devicerecord.physicalinterface.create(intf,container_uuid=containerID)
    
def create_vr(fmc,containerID,folderpath):
    vrfilepath = os.path.join(folderpath, "vr.json")
    with open(vrfilepath, mode="r") as file:
        data = json.load(file)
    get_name_id_mapping(data)
    for vr in data:
        print(f"Creating VR with name {vr["name"]} and id {vr["id"]}")
        fmc.device.devicerecord.routing.virtualrouter.create(vr,container_uuid=containerID)
        write_vr_id(vr["id"], folderpath=folderpath)

def create_vr_ipv4staticroutes(fmc,containerID,basedirectory):
    VR = fmc.device.devicerecord.routing.virtualrouter.get(container_uuid=containerID)
    for vr in VR:
         write_vr_id(vr["id"], folderpath="output/VirtualRouters")
    if os.path.exists(basedirectory): #output/VR exists
        for vr_name in os.listdir(basedirectory): #Folders under VR exists
            vr_path = os.path.join(basedirectory, vr_name) # Example /output/Client
            if os.path.isdir(vr_path): # if /output/Client is a directory
                ipv4staticroutefile = os.path.join(vr_path, "ipv4staticroute.json") # = /output/Client/ipv4staticroute.json
                
                vr_id = get_vrid(vr_path)
                with open(ipv4staticroutefile, "r") as file:
                    vr_routes = json.load(file)
                
                for vr_route in vr_routes:
                    if vr_id and is_valid_static_route_file(ipv4staticroutefile):
                        fmc.device.devicerecord.routing.virtualrouter.ipv4staticroute.create(vr_route,child_container_uuid=vr_id,container_uuid=containerID)


def create_vr_ecmpzones(fmc,containerID,basedirectory):
    VR = fmc.device.devicerecord.routing.virtualrouter.get(container_uuid=containerID)

    if os.path.exists(basedirectory): #output/VR exists
        for vr_name in os.listdir(basedirectory): #Folders under VR exists
            vr_path = os.path.join(basedirectory, vr_name) # Example /output/Client
            if os.path.isdir(vr_path): # if /output/Client is a directory
                ecmpzonefile = os.path.join(vr_path, "ecmp.json") # = /output/Client/ipv4staticroute.json
                
                vr_id = get_vrid(vr_path)
                with open(ecmpzonefile, "r") as file:
                    vr_routes = json.load(file)
                
                for vr_route in vr_routes:
                    if vr_id and is_valid_static_route_file(ecmpzonefile):
                        fmc.device.devicerecord.routing.virtualrouter.ecmpzone.create(vr_route,child_container_uuid=vr_id,container_uuid=containerID)

def create_vr_bgp(fmc,containerID,basedirectory):
    if os.path.exists(basedirectory): #output/VR exists
        for vr_name in os.listdir(basedirectory): #Folders under VR exists
            vr_path = os.path.join(basedirectory, vr_name) # Example /output/Client
            if os.path.isdir(vr_path): # if /output/Client is a directory
                bgproutefile = os.path.join(vr_path, "bgproutes.json") # = /output/Client/ipv4staticroute.json
                vr_id = get_vrid(vr_path)
                if vr_id and (is_valid_static_route_file(bgproutefile)):
                    
                    with open(bgproutefile, "r") as file:
                        bgp_routes = json.load(file)
                    
                    for bgp_route in bgp_routes:
                            #print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Creating route {bgp_route["name"]}")
                            fmc.device.devicerecord.routing.virtualrouter.bgp.create(bgp_route,child_container_uuid=vr_id,container_uuid=containerID)
