# Simple Minecraft Server Manager
# By Doomlad
# 07/01/2020

__version__ = '1.0.7'
import glob
from modules.config_gen import configuration
jar_files = []


def menu():
    print("\n[!]-----------------------------------[!]\n" +
          "[!]-=[Simple MCServer Manager " + __version__ + "]=-[!]\n"
          "[!]-----------------------------------[!]\n\n"
          "A simple local minecraft server management tool.\n")

    for file in glob.glob("*.jar"):
        jar_files.append(file)

    if len(jar_files) == 0:
        start_server = f"Start Server       (Server Jar: Not Found...)"
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
