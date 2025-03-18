import os
import json
from utils.utility import *
from datetime import datetime

def create_vr(fmc,containerID,folderpath):
    vrfilepath = os.path.join(folderpath, "vr.json")
    with open(vrfilepath, mode="r") as file:
        data = json.load(file)
    for vr in data:
        print(f"Creating VR with name {vr["name"]} and id {vr["id"]}")
        fmc.device.devicerecord.routing.virtualrouter.create(vr,container_uuid=containerID)

def create_vr_ipv4staticroutes(fmc,containerID,basedirectory):
    VR = fmc.device.devicerecord.routing.virtualrouter.get(container_uuid=containerID)

    if os.path.exists(basedirectory): #output/VR exists
        for vr_name in os.listdir(basedirectory): #Folders under VR exists
            vr_path = os.path.join(basedirectory, vr_name) # Example /output/Client
            if os.path.isdir(vr_path): # if /output/Client is a directory
                vrid_file = os.path.join(vr_path, "vrid.json") # vrif_file = /output/Client/vr.json
                ipv4staticroutefile = os.path.join(vr_path, "ipv4staticroute.json") # = /output/Client/ipv4staticroute.json
                
                vr_id = get_vrid(vrid_file)
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
                vrid_file = os.path.join(vr_path, "vrid.json") # vrif_file = /output/Client/vr.json
                ecmpzonefile = os.path.join(vr_path, "ecmp.json") # = /output/Client/ipv4staticroute.json
                
                vr_id = get_vrid(vrid_file)
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
                vrid_file = os.path.join(vr_path, "vrid.json") # vrif_file = /output/Client/vr.json
                bgproutefile = os.path.join(vr_path, "bgproutes.json") # = /output/Client/ipv4staticroute.json
                vr_id = get_vrid(vrid_file)
                if vr_id and (is_valid_static_route_file(bgproutefile)):
                    
                    with open(bgproutefile, "r") as file:
                        bgp_routes = json.load(file)
                    
                    for bgp_route in bgp_routes:
                            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Creating route {bgp_route["name"]}")
                            fmc.device.devicerecord.routing.virtualrouter.bgp.create(bgp_route,child_container_uuid=vr_id,container_uuid=containerID)
