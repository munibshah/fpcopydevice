import yaml
import os
import json
from typing import List, Dict,Any

def get_phyintf(fmc,containerID,folderpath="interfaces.yaml"):
    data = fmc.device.devicerecord.physicalinterface.get(container_uuid=containerID)
    json_converted_data=[]
    for obj in data:
        extracted_data={
            "id": obj.get("id"),
            "name": obj.get("name"),
            "ifname": obj.get("ifname"),
            "enabled": obj.get("enabled"),
            "type" : obj.get("type"),
            "mode": obj.get("mode"),
            "MTU": obj.get("MTU"),
            "ipv4": obj.get("ipv4"),
            "securityZone": obj.get("securityZone")
        }
        json_converted_data.append(extracted_data)
    yaml_string = yaml.dump(json_converted_data, default_flow_style=False, sort_keys=False)
    json_string = json.dumps(json_converted_data,indent=2)

    # Writing to files
    phyfilepath = os.path.join(folderpath, "phyintf.json")
    mode = "a" if os.path.isfile(folderpath) else "w"
    with open(phyfilepath, mode) as f:
        f.write(yaml_string)

    phyjsonpath = os.path.join(folderpath, "phyintf.json")
    mode = "a" if os.path.isfile(folderpath) else "w"
    with open(phyjsonpath,mode) as f:
        f.write(json_string)

def get_subintf(fmc,containerID,folderpath="interfaces.yaml"):
    data = fmc.device.devicerecord.subinterface.get(container_uuid=containerID)
    #Extract relevant JSON 
    json_converted_data = []
    for obj in data:
        converted_entry = {
            'name': obj.get('name'),
        'subIntfId': obj.get('subIntfId'),
        'vlanId': obj.get('vlanId'),
        'ifname': obj.get('ifname'),
        'id': obj.get('id'),
        'type': obj.get('type'),
        'enabled': obj.get('enabled'),
        'ipv4': {
            'static': {
                'address': obj.get('ipv4', {}).get('static', {}).get('address'),
                'netmask': obj.get('ipv4', {}).get('static', {}).get('netmask')
            }
        },
        'securityZone': {
            'id': obj.get('securityZone', {}).get('id'),
            'type': 'SecurityZone'
        },
        'managementOnly': obj.get('managementOnly'),
        }
        json_converted_data.append(converted_entry)


    #Converting Dict to strings so we can write them using f.write
    yaml_string = yaml.dump(json_converted_data, default_flow_style=False, sort_keys=False)
    json_string = json.dumps(json_converted_data,indent=2)

    # Writing to files
    subfilepath = os.path.join(folderpath, "subintf.yaml")
    mode = "w"
    with open(subfilepath, mode) as f:
        f.write(yaml_string)
    subjsonpath = os.path.join(folderpath, "subintf.json")
    mode = "w"
    with open(subjsonpath,mode) as f:
        f.write(json_string)


def get_etherintf(fmc,containerID,folderpath="interfaces.yaml"):
    data = fmc.device.devicerecord.etherchannelinterface.get(container_uuid=containerID)
    # Build a minimal dictionary with the fields you want.
    json_converted_data = []
    for obj in data: 
        converted_data = {
        "name": obj.get("name"),
        "enabled": obj.get("enabled"),
        "mode": obj.get("mode"),
        "id": obj.get("id"),
        "MTU": obj.get("MTU"),
        "etherChannelId": obj.get("etherChannelId"),
        "managementOnly": obj.get("managementOnly"),
        "ipv4": {
            "static": {
                "address": obj.get("ipv4", {}).get("static", {}).get("address"),
                "netmask": obj.get("ipv4", {}).get("static", {}).get("netmask")
            }
        }
        }
        json_converted_data.append(converted_data)
    yaml_string = yaml.dump(json_converted_data, default_flow_style=False, sort_keys=False)
    json_string = json.dumps(json_converted_data,indent=2)

    # Append this minimal object to the YAML file as a new document
    etherfilepath = os.path.join(folderpath, "etherintf.yaml")
    mode = "a" if os.path.isfile(folderpath) else "w"
    with open(etherfilepath, mode) as f:
        f.write(yaml_string)
    etherjsonpath = os.path.join(folderpath, "etherintf.json")
    mode = "a" if os.path.isfile(folderpath) else "w"
    with open(etherjsonpath,mode) as f:
        f.write(json_string)

def get_vr(fmc, containerID,folderpath="output"):
    virtualrouters=fmc.device.devicerecord.routing.virtualrouter.get(container_uuid=containerID)
    json_converted_data=[]
    for obj in virtualrouters:
        if obj.get("name") != "Global":
            minimal_obj = {
            "name": obj.get("name"),
            "id": obj.get("id"),
            "interfaces": obj.get("interfaces", [])
            }
            json_converted_data.append(minimal_obj)

    json_string = json.dumps(json_converted_data,indent=2)
    yaml_string = yaml.dump(json_converted_data, default_flow_style=False, sort_keys=False)

    yamlfilepath = os.path.join(folderpath, "vr.yaml")
    with open(yamlfilepath, "w") as f:
        f.write(yaml_string)
    jsonfilepath = os.path.join(folderpath, "vr.json")
    with open(jsonfilepath, "w") as f:
        f.write(json_string)
    return(virtualrouters)

def get_vr_ipv4staticroutes(fmc,containerID, vr_id, folderpath="output",vridonly=False):
    ipv4staticroute=fmc.device.devicerecord.routing.virtualrouter.ipv4staticroute.get(container_uuid=containerID,child_container_uuid=vr_id)
    json_converted_data=[]
    for obj in ipv4staticroute:
        minimal_obj = {
                "interfaceName": obj.get("interfaceName"),
                "selectedNetworks": obj.get("selectedNetworks", []),
                "metricValue": obj.get("metricValue"),
                "type": obj.get("type"),
                "id": obj.get("id")
            }
        gateway = obj.get("gateway", [])
        if gateway:  # Only add if not empty
            minimal_obj["gateway"] = gateway
        json_converted_data.append(minimal_obj)
    
    id_obj = {
            "id": vr_id
        }
    json_string = json.dumps(json_converted_data,indent=2)
    yaml_string = yaml.dump(json_converted_data, default_flow_style=False, sort_keys=False)
    vr_string = json.dumps(id_obj,indent=2) #To save VR_ID in the folder 

    #Write to different files under the VRF folder 
    if vridonly==False:
        yamloutput = os.path.join(folderpath, "ipv4staticroute.yaml")
        with open(yamloutput, "a") as f:
            f.write(yaml_string)
        jsonoutput = os.path.join(folderpath, "ipv4staticroute.json")
        with open(jsonoutput, "a") as f:
            f.write(json_string)
        vridoutput = os.path.join(folderpath, "vrid.json")
        with open(vridoutput, "w") as f:
            f.write(vr_string)
    elif vridonly==True:
        vridoutput = os.path.join(folderpath, "vrid.json")
        with open(vridoutput, "w") as f:
            f.write(vr_string)



def get_vr_bgproutes(fmc,containerID, vr_id, folderpath="bgp.yaml",vridonly=False):
    # Extract minimal BGP details while maintaining nesting
    bgproutes = fmc.device.devicerecord.routing.virtualrouter.bgp.get(container_uuid=containerID,child_container_uuid=vr_id)
    
    json_converted_data=[]
    for obj in bgproutes:
        minimal_obj = {
            "id": obj.get("id"),
            "asNumber": obj.get("asNumber"),
            "addressFamilyIPv4": {
                "distance": obj.get("addressFamilyIPv4", {}).get("distance"),
                "defaultInformationOrginate": obj.get("addressFamilyIPv4", {}).get("defaultInformationOrginate"),
                "bgpSupressInactive": obj.get("addressFamilyIPv4", {}).get("bgpSupressInactive"),
                "synchronization": obj.get("addressFamilyIPv4", {}).get("synchronization"),
                "bgpRedistributeInternal": obj.get("addressFamilyIPv4", {}).get("bgpRedistributeInternal"),
                "maximumPaths": obj.get("addressFamilyIPv4", {}).get("maximumPaths"),
                "neighbors": obj.get("addressFamilyIPv4", {}).get("neighbors"),
                "networks": obj.get("addressFamilyIPv4", {}).get("networks"),
                "routeImportExport": obj.get("addressFamilyIPv4", {}).get("routeImportExport"),
                "ebgp": obj.get("addressFamilyIPv4", {}).get("ebgp"),
                "ibgp": obj.get("addressFamilyIPv4", {}).get("ibgp"),
            }
        }
        json_converted_data.append(minimal_obj)
    id_obj = {
            "id": vr_id
        }
    
    json_string = json.dumps(json_converted_data,indent=2)
    yaml_string = yaml.dump(json_converted_data, default_flow_style=False, sort_keys=False)
    vr_string = json.dumps(id_obj,indent=2) #To save VR_ID in the folder 

    #Write to different files under the VRF folder
    if vridonly==False:
        yamloutput = os.path.join(folderpath, "bgproutes.yaml")
        with open(yamloutput, "a") as f:
            f.write(yaml_string)
        jsonoutput = os.path.join(folderpath, "bgproutes.json")
        with open(jsonoutput, "a") as f:
            f.write(json_string)
        vridoutput = os.path.join(folderpath, "vrid.json")
        with open(vridoutput, "w") as f:
            f.write(vr_string)
    elif vridonly==True:
        vridoutput = os.path.join(folderpath, "vrid.json")
        with open(vridoutput, "w") as f:
            f.write(vr_string)

def get_vr_ecmpzones(fmc,containerID, vr_id, folderpath="ecmpzones.yaml",vridonly=False):
    ecmpzone = fmc.device.devicerecord.routing.virtualrouter.ecmpzones.get(container_uuid=containerID,child_container_uuid=vr_id)

    #print(ecmpzone)
    # Build the minimal dictionary with the keys you want in your YAML

    json_converted_data=[]
    for obj in ecmpzone:
        # Ensure interfaces exist and are extracted properly
        minimal_obj = {
                "name": obj.get("name"),
                "id": obj.get("id"),
                "type": obj.get("type"),
                "interfaces": [
                    {
                        "ifname": iface.get("ifname"),
                        "id": iface.get("id"),
                        "name": iface.get("name"),
                        "type": iface.get("type")
                    } for iface in obj.get("interfaces", [])
                ]
            }
        json_converted_data.append(minimal_obj)

    id_obj = {
            "id": vr_id
        }
    
    json_string = json.dumps(json_converted_data,indent=2)
    yaml_string = yaml.dump(json_converted_data, default_flow_style=False, sort_keys=False)
    vr_string = json.dumps(id_obj,indent=2) #To save VR_ID in the folder 

    #Write to different files under the VRF folder
    if vridonly==False:
        yamloutput = os.path.join(folderpath, "ecmp.yaml")
        with open(yamloutput, "a") as f:
            f.write(yaml_string)
        jsonoutput = os.path.join(folderpath, "ecmp.json")
        with open(jsonoutput, "a") as f:
            f.write(json_string)
        vridoutput = os.path.join(folderpath, "vrid.json")
        with open(vridoutput, "w") as f:
            f.write(vr_string)
    if vridonly==True:
        vridoutput = os.path.join(folderpath, "vrid.json")
        with open(vridoutput, "w") as f:
            f.write(vr_string)

def get_name_id_mapping(fmc,containerID,childID="subintf") -> Dict[str, str]:
    """
    Extract name to ID mapping from the GET output data.
    """
    if childID == "subintf":
        data = fmc.device.devicerecord.subinterface.get(container_uuid=containerID)
    name_id_map = {}
    for interface in data:
        if 'ifname' in interface and 'id' in interface:
            name_id_map[interface['ifname']] = interface['id']
    return name_id_map