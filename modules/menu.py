# Simple Minecraft Server Manager
# By Doomlad
# 07/01/2020

# Imports
import glob
from modules.config_gen import configuration

# Global vars
__version__ = '1.0.8-pre2'  # Version
pre_release = True  # Whether current version is a pre-release
jar_files = []  # Jars array


def menu():
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
                "[!] please download full releases. These builds are usually\n" \
                "[!] for testing purposes in between release builds. Thank you.\n"

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
        jar_files.append(file)

    # If there's none, print not found
    if len(jar_files) == 0:
        start_server = f"Start Server       (Server Jar: Not Found...)"

    # If there are, TODO: extract the jar file and look for version information
    else:
        start_server = f"Start Server       (Server Jar: {jar_files[0]}...[OK])"

    settings = f"Settings           (Ram: " + configuration.ram + "GB)"
    server_jar_manager = f"Server Jar Manager "
    backups = f"Backups "
    exit_code = f"Exit "

    menu.menu_items = [start_server, settings, server_jar_manager, backups, exit_code]
    menu_counter = 0
    for item in menu.menu_items:
        menu_counter += 1
        print("[" + str(menu_counter) + "] » " + item)
