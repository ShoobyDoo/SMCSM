## Simple Minecraft Server Manager

![Donate](https://img.shields.io/badge/Donate-Coffee-green?style=for-the-badge&logo=buy-me-a-coffee)

#### A cross platform server management script written entirely in Python.

![SMCSM](https://cdn.discordapp.com/attachments/584258352859709450/733456193372291133/6284fbc66f7d7602d8ce15dd5819c9d7.png)
 
---

### Features
* Compatible with Windows and Linux
* Most efficient set of jvm arguments to run server
* Easily handle ram dedication in script
* Choose to auto-start server upon script launch
* Auto-restart on crash/stop
* In-app Paper.io jar download + installer
* Rudimentary backup manager (exports to .zip)
* Bypass auto-start to access program normally
* Even more optimizations for bukkit, spigot, and paper.yml files
 
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

#### Linux Installation
*Installation steps for your specific environment may vary. I only cover Ubuntu here.*

Please run `sudo apt-get update` before beginning to ensure you're up to date.

    Installation Guide (Linux):
    
    Step 1. sudo apt-get install python3-setuptools default-jre python3-pip
    Step 2. sudo python3 -m pip install PyYAML progress
  
Once all prerequisites are satisfied, simply copy the script and modules folder to your server directory and 
run with `sudo python3 smcsm.py`
 
---

#### Windows Installation

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
