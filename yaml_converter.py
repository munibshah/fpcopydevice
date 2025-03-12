import yaml
from collections import OrderedDict

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
        'ifname': obj['ifname'],
        'name': obj['name'],
        'id': obj['metadata']['domain']['id'],  # or obj['id'] if you want the interface ID
        'type': obj['type'],
        'MTU': obj['MTU'],
        'enabled': obj['enabled'],
        'managementOnly': obj['managementOnly'],
    }
    yaml_string = yaml.dump(minimal_obj, default_flow_style=False, sort_keys=False)
    print(yaml_string)
    # Append this minimal object to the YAML file as a new document
    with open(filepath, "w") as f:
        # The 'explicit_start=True' ensures that each appended block 
        # starts with "---", creating multiple YAML documents in one file
        f.write("\n---\n")
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
        'ifname': obj.get('ifname'),
        'name': obj.get('name'),
        'id': obj.get('id'),
        'type': obj.get('type'),
        'enabled': obj.get('enabled'),
        'vlanId': obj.get('vlanId'),
        'subIntfId': obj.get('subIntfId'),
        'ipv4address': obj.get('ipv4', {}).get('static', {}).get('address'),
        'ipv4netmask': obj.get('ipv4', {}).get('static', {}).get('netmask'),
        'securityZoneId': obj.get('securityZone', {}).get('id'),
        'managementOnly': obj.get('managementOnly'),
    }
    yaml_string = yaml.dump(minimal_obj, default_flow_style=False, sort_keys=False)
    print(yaml_string)
    # Append this minimal object to the YAML file as a new document
    with open(filepath, "a") as f:
        # The 'explicit_start=True' ensures that each appended block 
        # starts with "---", creating multiple YAML documents in one file
        f.write("\n---\n")
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
        'ifname': obj.get('ifname'),  # Some EtherChannel objects may not have 'ifname'
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
    print(yaml_string)
    # Append this minimal object to the YAML file as a new document
    with open(filepath, "a") as f:
        # The 'explicit_start=True' ensures that each appended block 
        # starts with "---", creating multiple YAML documents in one file
        f.write("\n---\n")
        f.write(yaml_string)
        f.write("\n")