## Simple Minecraft Server Manager

[![Donate](https://img.shields.io/badge/Donate-grey?style=for-the-badge&logo=buy-me-a-coffee)](https://www.buymeacoffee.com/doomlad)

#### A cross platform server management script written entirely in Python.

![SMCSM](https://cdn.discordapp.com/attachments/795701802208985140/803404147256852520/70e36ed1d8185ee918a5a541d4b7af8b.png)
 
---

### Features
* Compatible with Windows and Linux
* Most startup script arguments to run server [(Aikars JVM Flags)](https://aikar.co/2018/07/02/tuning-the-jvm-g1gc-garbage-collector-flags-for-minecraft/).
* Easily handle ram dedication in script
* Choose to auto-start server upon script launch
* Auto-restart on crash/stop
* In-app Paper.io jar download + installer
* Robust and detailed backups manager
* Bypass auto-start to access program normally
* Even more optimizations for bukkit, spigot, and paper.yml files
* Version management for your server jars (Currently supports only paper.io jars)
* Automatically accepts server eula + complete install of jar (All files generated at the press of an enter key :))

### Upcoming Features (1.0.8+)
* Playit.gg integration (Anyone can host their OWN Minecraft server PUBLICALLY for FREE)
* Other various online features: In-app server list, ping statistics, potential RCON support. (Stay tuned!)
* Install backup.zips seemlessly
* Setup automatic backups on certain date/time
---
 
### Requirements
* Requires [Java](https://www.java.com/en/download/).
* Requires [Python 3.6](https://www.python.org/downloads/) or higher.
* Requires [PyYAML](https://pypi.org/project/PyYAML/) for server optimizer feature
* Requires [progress](https://pypi.org/project/progress/) for progress bar when zipping backups
 
---
### Installation

> #### Automatic Installation

#### Windows
Step 1. Head over to the [Releases](https://github.com/Doomlad/SMCSM/releases) and download the latest `smcsm-XXX_win64.exe` file.

Step 2. Copy the file into server directory and run.

#### Linux
Step 1. Head over to the [Releases](https://github.com/Doomlad/SMCSM/releases) and download the latest `smcsm-XXX_linux` file.

Step 2. Copy the file into server directory and run the file by running `./smcsm-XXX_linux` in the terminal.

*Please note: There might be some issues getting the program to run initially with dependencies, so please refer to the guide below and execute Steps 1 & 2 in the terminal.*

---

> #### Manual Installation

#### Linux
*Installation steps for your specific environment may vary. I only cover Ubuntu here.*

Please run `sudo apt-get update` before beginning to ensure you're up to date.

    Installation Guide (Linux):
    
    Step 1. sudo apt-get install python3-setuptools default-jre python3-pip
    Step 2. sudo python3 -m pip install PyYAML progress
  
Once all prerequisites are satisfied, simply copy the script and modules folder to your server directory and 
run with `sudo python3 smcsm.py`
 
---

#### Windows

*Please note: Python on the Windows terminal is accessed with `py` instead of `python`. In the event that*
*you are having issues accessing python 3, try `py -3` instead.*

    Installation Guide (Windows):
    
    Step 1. Install the latest versions of both Java and Python 3 (64 bit)
    Step 2. Once Python is installed, you should be able to run smcsm.py by just double-clicking on it
    Step 3. Ensure you copy both the modules folder and smcsm.py into your server folder  

Once all prerequisites are satisfied, simply double-click smcsm.py to start the program.

---

### Support & Discussion
I can offer realtime support and discussion over on my [Discord Server](https://discord.gg/cuRC9pN)
