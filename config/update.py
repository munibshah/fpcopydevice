import os
import json
from utils.utility import *
from datetime import datetime
import sys
from typing import Dict


def update_vr_with_intfid(name_id_map: Dict[str, str]) -> None:
    vr_file_path = 'output/vr.json'

    if not os.path.exists(vr_file_path):
        print(f"Error: {vr_file_path} not found.")
        sys.exit(1)

    try:
        # Read the vr.json file
        with open(vr_file_path, 'r') as f:
            vr_data = json.load(f)
        
        # Track if we made any updates
        updates_made = False

        for vr in vr_data:
            if 'interfaces' in vr:
                for interface in vr['interfaces']:
                    if 'name' in interface and interface['name'] in name_id_map:
                        # Update the ID based on the name mapping
                        old_id = interface['id']
                        new_id = name_id_map[interface['name']]
                        if old_id != new_id:
                            print(f"Updating interface with name '{interface['name']}' ID from {old_id} to {new_id}")
                            interface['id'] = new_id
                            updates_made = True
        
        if updates_made:
            # Save the updated vr.json file
            with open(vr_file_path, 'w') as f:
                json.dump(vr_data, f, indent=2)
            print(f"Successfully updated {vr_file_path}")
        else:
            print("No updates were needed.")
    
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {vr_file_path}")
        sys.exit(1)
    
    except IOError as e:
        print(f"Error writing to {vr_file_path}: {e}")
        sys.exit(1)