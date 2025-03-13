from fireREST import FMC
import logging
import yaml
import os 
import shutil
from yaml_converter import phyintf_yaml,etherintf_yaml,subintf_yaml,vr_yaml,vr_routes_yaml,vr_bgp_routes_yaml,vr_ecmpzones_yaml
from cleanfile import clear_output_folder


host = ""
username = ""
password = ""
ftdname = ""

clear_output_folder("output")

fmc = FMC(hostname=host, username=username, password=password, domain='Global')
Device = fmc.device.devicerecord.get(name=ftdname)
containerID = Device.get('id')
EtherIntf = fmc.device.devicerecord.etherchannelinterface.get(container_uuid=containerID)
SubIntf = fmc.device.devicerecord.subinterface.get(container_uuid=containerID)
PhyIntf = fmc.device.devicerecord.physicalinterface.get(container_uuid=containerID)

for interface in EtherIntf:
    print(interface)
    etherintf_yaml(interface,filepath="output/etherchannelintf.yaml")

for interface in SubIntf:
    print(interface)
    subintf_yaml(interface,filepath="output/subintf.yaml")

for interface in PhyIntf:
    print(interface)
    phyintf_yaml(interface,filepath="output/phyintf.yaml")

virtualrouters=fmc.device.devicerecord.routing.virtualrouter.get(container_uuid=containerID)
vr_list =[]
for vr in virtualrouters:
    vr_list.append({"name": vr["name"], "id": vr["id"]})
    vrname = vr["name"]
    ipv4staticroute=fmc.device.devicerecord.routing.virtualrouter.ipv4staticroute.get(container_uuid=containerID,child_container_uuid=vr["id"])
    bgproutes = fmc.device.devicerecord.routing.virtualrouter.bgp.get(container_uuid=containerID,child_container_uuid=vr["id"])
    ecmpzone = fmc.device.devicerecord.routing.virtualrouter.ecmpzones.get(container_uuid=containerID,child_container_uuid=vr["id"])
    print(vr["name"])
    print(ecmpzone)
    vr_yaml(vr,filepath="output/vr.yaml")
    for route in ipv4staticroute:
        directory =f"output/{vr["name"]}"
        os.makedirs(directory, exist_ok=True)
        vr_routes_yaml(route,filepath=f"output/{vr["name"]}/ipv4staticroute.yaml")
    for route in bgproutes:
        directory =f"output/{vr["name"]}"
        os.makedirs(directory, exist_ok=True)
        vr_bgp_routes_yaml(route,filepath=f"output/{vr["name"]}/bgproutes.yaml")
    for zone in ecmpzone:
        directory =f"output/{vr["name"]}"
        os.makedirs(directory, exist_ok=True)
        vr_ecmpzones_yaml(route,filepath=f"output/{vr["name"]}/ecmp.yaml")


# for vr in vr_list:
#     vrid = vr["id"]  # The ID to pass as 'child_container_name'
#     vr_name = vr["name"]
#     print(vr_name)
#     ipv4staticroute=fmc.device.devicerecord.routing.virtualrouter.ipv4staticroute.get(container_uuid=containerID,child_container_uuid=vrid)
#     print(ipv4staticroute)

#     for route in ipv4staticroute:
#         vr_routes_yaml(route,filepath="output/vr-routes.yaml")
    # Call the FMC library method using the router's ID
    # virtualrouters = fmc.device.devicerecord.routing.virtualrouter.ipv4staticroute.get(
    #     container_uuid=containerID,
    #     child_container_name=vrid
    # )
    
    # Do something with the returned data
    #print(f"Virtual Router: {vr_name} (ID: {vrid}) => Result: {virtualrouters}")