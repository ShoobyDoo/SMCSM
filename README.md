## Simple Minecraft Server Manager
##### A cross platform server management script written entirely in Python.

![SMCSM](https://cdn.discordapp.com/attachments/584258352859709450/733456193372291133/6284fbc66f7d7602d8ce15dd5819c9d7.png)
 
---

### Features
* Compatible with Windows and Linux
* Most efficient set of arguments to run server
* Easily handle ram dedication in script
* Automatically choose to start server upon script launch
* Automatically restart when server closes/crashes
* In-app Paper.io jar download + installer
 
---
 
### Requirements
* Requires [Java](https://www.java.com/en/download/).
* Requires [Python 3.6](https://www.python.org/downloads/) or higher.
* Requires [PyYAML](https://pypi.org/project/PyYAML/) for server optimizer feature
* Requires [progress](https://pypi.org/project/progress/) for progress bar when zipping backups
 
---

#### Linux Installation
*Installation steps specific environment may vary. I only cover Ubuntu here.*

Please run `sudo apt-get update` before beginning to ensure you're up to date.

    Installation Guide (Linux):
    
    Step 1. sudo apt-get install python3-setuptools
    Step 2. sudo apt-get install default-jre (Most cases this will work)
    Step 3. sudo apt-get install python3-pip
    Step 4. sudo python3 -m pip install PyYAML
    Step 5. sudo python3 -m pip install progress
  
Once all prerequisites are satisfied, simply copy the script to your server directory and 
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
