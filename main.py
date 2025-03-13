from fireREST import FMC
import logging
import yaml
import os 
import shutil
from yaml_converter import phyintf_yaml,etherintf_yaml,subintf_yaml
from cleanfile import clear_output_folder


host = "10.8.63.91"
username = "admin"
password = "CXlabs.123"
ftdname = "pdx1-co-pop-fw1"

clear_output_folder("output")

fmc = FMC(hostname=host, username=username, password=password, domain='Global')
Device = fmc.device.devicerecord.get(name="pdx1-co-pop-fw1")
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

