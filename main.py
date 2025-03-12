"""
Unit testing, of a sort, all the created methods/classes.
"""

import fmcapi
import logging
import unit_tests
import yaml
from collections import OrderedDict
from yaml_converter import phyintf_yaml,etherintf_yaml,subintf_yaml


# ### Set these variables to match your environment. ### #

host = "1.1.1.1"
username = "admin"
password = "Cisco123"
autodeploy = False
logname = "TestingUserScript.log"
pagelimit = 500
debug = False
ftdname = ""

def main():
    with fmcapi.FMC(
        host=host,
        username=username,
        password=password,
        autodeploy=autodeploy,
        limit=pagelimit,
        file_logging=logname,
        debug=debug,
    ) as fmc1:
        
        # Initiate DeviceRecords
        ftd = fmcapi.DeviceRecords(fmc=fmc1)
        ftd.get(name=ftdname)

        #Call interfaces and save it under interfacec.yaml
        ftd_phyintf = fmcapi.PhysicalInterfaces(fmc=fmc1, device_name=ftd.name)
        ftd_subintf= fmcapi.SubInterfaces(fmc=fmc1, device_name=ftd.name)
        ftd_etherintf = fmcapi.EtherchannelInterfaces(fmc=fmc1, device_name=ftd.name)
        print("\n")
        for interface in ftd_phyintf.get()["items"]: 
            phyintf_yaml(interface,filepath="interfaces.yaml")
        for interface in ftd_subintf.get()["items"]: 
            subintf_yaml(interface,filepath="interfaces.yaml")
        for interface in ftd_etherintf.get()["items"]: 
            etherintf_yaml(interface,filepath="interfaces2.yaml")

if __name__ == "__main__":
    main()
