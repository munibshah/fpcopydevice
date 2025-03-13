import yaml
import os

def phyintf_yaml(obj, filepath="interfaces.yaml"):
    """
    Extracts specific fields from the given dictionary, converts them to YAML,
    and appends as a new document to the specified file.

    :param obj: The original interface dictionary
    :param filepath: Name/path of the YAML file to append to
    """

    # Build the minimal dictionary with the keys you want in your YAML
    # (Assuming you want the 'id' from the domain, since that's what
    #  you stated in your example. If you want the interface's ID, replace
    #  obj['metadata']['domain']['id'] with obj['id'].)
    minimal_obj = {
        'name': obj['name'],
        'id': obj['metadata']['domain']['id'],  # or obj['id'] if you want the interface ID
        'type': obj['type'],
        'MTU': obj['MTU'],
        'enabled': obj['enabled'],
        'ipv4address': obj.get('ipv4', {}).get('static', {}).get('address'),
        'ipv4netmask': obj.get('ipv4', {}).get('static', {}).get('netmask'),
        'securityZoneId': obj.get('securityZone', {}).get('id'),
        'managementOnly': obj['managementOnly'],
    }
    mode = "a" if os.path.isfile(filepath) else "w"
    yaml_string = yaml.dump(minimal_obj, default_flow_style=False, sort_keys=False)
    #print(yaml_string)
    # Append this minimal object to the YAML file as a new document
    with open(filepath, mode) as f:
        # The 'explicit_start=True' ensures that each appended block 
        # starts with "---", creating multiple YAML documents in one file
        # f.write("\n---\n")
        f.write(yaml_string)
        f.write("\n")

def subintf_yaml(obj, filepath="interfaces.yaml"):
    """
    Extracts specific fields from the given SubInterface dictionary,
    converts them to YAML, and appends the resulting YAML string
    (prefixed with "---") to the file.

    Fields captured:
      ifname
      name
      id
      type
      enabled
      vlanId
      subIntfId
      ipv4address
      ipv4netmask
      securityZoneId
      managementOnly
    """

    # Build a minimal dictionary with the fields you want.
    minimal_obj = {
        'name': obj.get('name'),
        'subIntfId': obj.get('subIntfId'),
        'vlanId': obj.get('vlanId'),
        'ifname': obj.get('ifname'),
        'id': obj.get('id'),
        'type': obj.get('type'),
        'enabled': obj.get('enabled'),
        'ipv4address': obj.get('ipv4', {}).get('static', {}).get('address'),
        'ipv4netmask': obj.get('ipv4', {}).get('static', {}).get('netmask'),
        'securityZoneId': obj.get('securityZone', {}).get('id'),
        'managementOnly': obj.get('managementOnly'),
    }
    mode = "a" if os.path.isfile(filepath) else "w"
    yaml_string = yaml.dump(minimal_obj, default_flow_style=False, sort_keys=False)
    #print(yaml_string)
    # Append this minimal object to the YAML file as a new document
    with open(filepath, mode) as f:
        # The 'explicit_start=True' ensures that each appended block 
        # starts with "---", creating multiple YAML documents in one file
        # f.write("\n---\n")
        f.write(yaml_string)
        f.write("\n")

def etherintf_yaml(obj, filepath="interfaces.yaml"):
    """
    Extracts specific fields from the given EtherChannelInterface dictionary,
    converts them to YAML, and appends the resulting YAML string
    (prefixed with "---") to the file.

    Fields captured (adjust as needed):
        ifname          (may not exist, so defaults to None)
        name
        id
        type
        enabled
        managementOnly
        etherChannelId
        ipv4address
        ipv4netmask
    """

    # Build a minimal dictionary with the fields you want.
    minimal_obj = {
        'name': obj.get('name'),
        'id': obj.get('id'),
        'type': obj.get('type'),
        'enabled': obj.get('enabled'),
        'managementOnly': obj.get('managementOnly'),
        'etherChannelId': obj.get('etherChannelId'),
        'ipv4address': obj.get('ipv4', {}).get('static', {}).get('address'),
        'ipv4netmask': obj.get('ipv4', {}).get('static', {}).get('netmask'),
    }
    yaml_string = yaml.dump(minimal_obj, default_flow_style=False, sort_keys=False)
    #print(yaml_string)
    # Append this minimal object to the YAML file as a new document
    with open(filepath, "a") as f:
        # The 'explicit_start=True' ensures that each appended block 
        # starts with "---", creating multiple YAML documents in one file
        # f.write("\n---\n")
        f.write(yaml_string)
        f.write("\n")

def vr_yaml(obj, filepath="interfaces.yaml"):
    """
    Extracts the VR name and ID from `obj`, then writes/appends them in YAML.
    If 'interfaces.yaml' does not exist, it creates a new file;
    otherwise, it appends as a new YAML document.
    """
    minimal_obj = {
        "name": obj.get("name"),
        "id": obj.get("id")
    }
    yaml_string = yaml.dump(minimal_obj, default_flow_style=False, sort_keys=False)
    #print(yaml_string)
    # Append this minimal object to the YAML file as a new document
    with open(filepath, "a") as f:
        # The 'explicit_start=True' ensures that each appended block 
        # starts with "---", creating multiple YAML documents in one file
        f.write("\n---\n")
        f.write(yaml_string)
        f.write("\n")

def vr_routes_yaml(obj, filepath="interfaces.yaml"):
    """
    Extract the desired IPv4 static route fields from 'obj'
    and write/append them in YAML format.

    Fields captured:
      egressInterfaceVirtualRouter,
      interfaceName,
      selectedNetworks,
      metricValue,
      type,
      id

    :param obj: A single IPv4 static route dictionary.
    :param filepath: Path to the YAML file (default: "interfaces.yaml").
    """

    # Build a minimal dictionary with the exact fields you want.
    minimal_obj = {
        "egressInterfaceVirtualRouter": obj.get("metadata", {}).get("egressInterfaceVirtualRouter"),
        "interfaceName": obj.get("interfaceName"),
        "selectedNetworks": obj.get("selectedNetworks"),
        "metricValue": obj.get("metricValue"),
        "type": obj.get("type"),
        "id": obj.get("id"),
    }
    yaml_string = yaml.dump(minimal_obj, default_flow_style=False, sort_keys=False)
    #print(yaml_string)
    # Append this minimal object to the YAML file as a new document
    with open(filepath, "a") as f:
        # The 'explicit_start=True' ensures that each appended block 
        # starts with "---", creating multiple YAML documents in one file
        # f.write("\n---\n")
        f.write(yaml_string)
        f.write("\n")


def vr_bgp_routes_yaml(obj, filepath="bgp.yaml"):
    """
    Extracts the desired BGP fields from 'obj' and writes/appends them in YAML format.

    Fields captured:
      - id
      - asNumber
      - addressFamilyIPv4:
        - distance
        - defaultInformationOrginate
        - bgpSupressInactive
        - synchronization
        - bgpRedistributeInternal
        - maximumPaths
        - neighbors
        - networks
        - routeImportExport
        - ebgp
        - ibgp

    :param obj: A single BGP dictionary.
    :param filepath: Path to the YAML file (default: "bgp.yaml").
    """

    # Extract minimal BGP details while maintaining nesting
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
    yaml_string = yaml.dump(minimal_obj, default_flow_style=False, sort_keys=False)
    #print(yaml_string)
    # Append this minimal object to the YAML file as a new document
    with open(filepath, "a") as f:
        # The 'explicit_start=True' ensures that each appended block 
        # starts with "---", creating multiple YAML documents in one file
        # f.write("\n---\n")
        f.write(yaml_string)
        f.write("\n")

def vr_ecmpzones_yaml(obj, filepath="ecmpzones.yaml"):
    """
    Extracts specific fields from the given dictionary, converts them to YAML,
    and appends as a new document to the specified file.

    :param obj: The original ECMP zone dictionary
    :param filepath: Name/path of the YAML file to append to
    """

    # Build the minimal dictionary with the keys you want in your YAML
    if isinstance(obj, list):
        obj_list = obj
    else:
        obj_list = [obj]

    # Build the minimal dictionary with the keys you want in your YAML
    yaml_data = []
    for item in obj_list:
        minimal_obj = {
            'name': item.get('name'),
            'id': item.get('id'),
            'type': item.get('type'),
            'interfaces': [
                {
                    'ifname': iface.get('ifname'),
                    'type': iface.get('type'),
                    'id': iface.get('id'),
                    'name': iface.get('name')
                }
                for iface in item.get('interfaces', [])
            ]
        }
        yaml_data.append(minimal_obj)
    # Append to YAML file
    yaml_string = yaml.dump(minimal_obj, default_flow_style=False, sort_keys=False)
    #print(yaml_string)
    # Append this minimal object to the YAML file as a new document
    with open(filepath, "a") as f:
        # The 'explicit_start=True' ensures that each appended block 
        # starts with "---", creating multiple YAML documents in one file
        # f.write("\n---\n")
        f.write(yaml_string)
        f.write("\n")