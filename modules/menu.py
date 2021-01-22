# Simple Minecraft Server Manager
# By Doomlad
# 07/01/2020

# Imports
import configparser
import glob
import json
from modules.config_gen import configuration
from modules.jar_downloader import get_latest_build_version

# Global vars
__version__ = '1.0.9-Pre7'

# Cheeky one liner :^)
pre_release = True if __version__.lower().find("-pre") != -1 else False  # Whether current version is a pre-release
# else: pre_release = False


def print_menu():

    # Jars array
    print_menu.jar_files = []

    # Create a space between pre-start checks
    print()

    # If pre-release is true
    if pre_release:
        banner = \
                "[-]--------------------------------------------[-]\n" \
                "[|]---=[Simple MCServer Manager " + __version__ + "]=---[|]\n" \
                "[-]--------------------------------------------[-]\n\n" \
                "A simple local minecraft server management tool.\n\n" \
                "[!] This is a pre-release version of SMCSM. For stability,\n" \
                "[!] please download full releases. These builds are for\n" \
                "[!] testing purposes in between release builds. Thank you.\n"

    # If pre-release is false
    else:
        banner = \
                "[-]---------------------------------------[-]\n" \
                "[|]---=[Simple MCServer Manager " + __version__ + "]=---[|]\n" \
                "[-]---------------------------------------[-]\n\n" \
                "A simple local minecraft server management tool.\n"

    # Print whichever of the two banners returns true
    print(banner)

    # Grab all files ending in .jar
    for file in glob.glob("*.jar"):
        print_menu.jar_files.append(file)

    ok_status = False
    out_of_date = False
    print_menu.mc_version = "Unknown"  # If version_history file doesn't exist

    # If No Jar found AND there's a valid jar in the list, remove the No Jar found entry
    for jar in print_menu.jar_files:
        if jar == "No jar found." and len(print_menu.jar_files) > 1:
            print_menu.jar_files.remove(jar)

    # If there's none, print not found
    if len(print_menu.jar_files) == 0:
        print_menu.jar_files.append("No jar found.")

    # If there is version_history.json, open and get jar version. Then present user with an update.
    else:
        try:
            # Read config
            config = configparser.ConfigParser()
            config.read("user_config.ini")
            with open("version_history.json") as vh:
                dump = json.load(vh)
            # JSON dump to var
            version_info = dump["currentVersion"]  # Returns git-Paper-1618 (MC: 1.12.2)

            # Split string
            build = version_info.split(" (MC: ")  # Makes git-Paper-1618 / (MC: 1.12.2)

            # Split further to extract minecraft version
            version = build[1].split(")")  # Returns near full version
            print_menu.mc_version = str(version[0])  # Trim remainder and assign to var

            # Split further to extract build number
            build = build[0].split("git-Paper-")  # Returns build
            paper_build = str(build[1])  # Assign build# to var

            # Write the version / build information to config
            config.set('Server Settings', print_menu.mc_version, paper_build)

            # Open config and write data in memory
            with open("user_config.ini", "w+") as configfile:
                config.write(configfile)
            configfile.close()

            # Check for latest build based off of version selected
            latest_build = get_latest_build_version(print_menu.mc_version)
            if int(paper_build) < int(latest_build):
                out_of_date = True

            # Update ok_status for start_server var condition
            ok_status = True

        except Exception:
            ok_status = False

    # Small check to ensure ok_status and jar is in date
    if ok_status and not out_of_date:
        for jars in print_menu.jar_files:
            if 'server' in jars:
                suffix = "[OK]"
            else:
                suffix = "[WARN: Is this a server jar?]"
        server_jar_manager = f"Server Jar Manager (Running latest build ({paper_build}) for version {print_menu.mc_version}!)"

    # If not, notify user that jar is out of date
    else:
        if "No jar found." in print_menu.jar_files:
            suffix = "[CRITICAL]"
            server_jar_manager = f"Server Jar Manager (Download Paper.io server jars from here!)"
        else:
            suffix = "[~OK]"
            if len(print_menu.jar_files) > 0 and print_menu.mc_version == "Unknown":
                server_jar_manager = f"Server Jar Manager (Don't know your version! Run server once.)"

            else:
                server_jar_manager = f"Server Jar Manager (Update available for version {print_menu.mc_version}!)"

    start_server = f"Start Server ({configuration.ram}GB) (Version: {print_menu.mc_version} ({print_menu.jar_files[0]})...{suffix})"

    settings = f"Settings           (Config: {configuration.config_status})"
    backups = f"Backups "
    exit_code = f"Exit "

    print_menu.menu_items = [start_server, settings, server_jar_manager, backups, exit_code]
    menu_counter = 0
    for item in print_menu.menu_items:
        menu_counter += 1
        print("[" + str(menu_counter) + "] » " + item)
