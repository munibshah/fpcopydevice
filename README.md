# FMC Device Copy Automation

## Overview

This repository contains Python scripts designed to interact with the Cisco Firepower Management Center (FMC) REST API to allow users to copy device configuration across multiple platforms. The FMC feature of device copy needs the source and destination device to be the same platform.  

---

## Scripts Included

| Script Name     | Description                                                                                   |
|-----------------|-----------------------------------------------------------------------------------------------|
| `main_get.py`    | Retrieves device specific settings such as interfaces, routes using the REST API.            |
| `main_delete.py` | Deletes specified FTD objects or policies by their unique ID.                                |
| `main_create.py` | Creates new objects and routes based on input JSON payloads or templates.                    |

---

## What works
+ Physical Interfaces 
+ Etherchannel Interfaces 
+ Subinterfaces 
+ Virtual Routers
+ IPv4 Static Routes
+ BGP Routes
+ ECMP Configuration

---

## Requirements

- Python 3.13+
- Required Python libraries:
  ```bash
  pip install -r requirements.txt
  ```
- Enable virtual environment
  ```bash
  source virtualenv/bin/activate
  ```
- `.env` file containing:
  ```
  HOST=https://<your-fmc-ip>
  USERNAME=<your-username>
  PASSWORD=<your-password>
  FTDNAME=<ftd-name>
  ```

> **Note:** Ensure your user account has the required API access permissions in FMC.

---

## Usage Examples


```bash
To be added
```

---

## Roadmap / TODO
- [ ] Support for ospfv2/3

---

## Contribution
Pull requests and feature requests are welcome. Please open an issue to discuss changes or improvements.

---

## License
[MIT License](LICENSE)

---

## Author
*Munib Shah*  
*Principal Architect / Cisco Services*  
