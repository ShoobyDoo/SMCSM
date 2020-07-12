# Simple Minecraft Server Manager
# By Doomlad
# 07/01/2020

import os
import configparser
import time
import glob
import platform
from modules.config_gen import configuration
from modules.menu import menu
from modules.clear_screen import clear_screen
from modules.jar_downloader import get_paper, get_latest_build_version, get_server_jar_versions

prefix = "[SMCSM] » "
config = configparser.ConfigParser()
yes_array = ['y', 'yes']


def main():
    configuration()
    while True:
        menu()
        config.read('user_config.ini')
        auto_start_status = config['Server Settings']['Auto Start']

        # Check auto_start_status
        if auto_start_status == 'true':

            try:
                counter = 3
                print("\n" + prefix + "Press [CTRL + C] to bypass auto-start. Executing in: ", end="", flush=True)
                for i in range(counter):
                    print(counter, end="\b", flush=True)
                    counter -= 1
                    time.sleep(1)

                print("Times up! Starting...", end="\b", flush=True)
                print()
                user_input = '1'

            except KeyboardInterrupt:
                user_input = input("\n" + prefix)
                pass

        else:
            user_input = input("\n" + prefix)

        # Start the Server
        if user_input == '1':

            if platform.system() == "Windows":
                print(prefix + "Current platform is Windows.")
                cmd_args = f'cmd /c "{str(configuration.optimized_start)}"'

            elif platform.system() == "Linux" or platform.system() == "Darwin":
                print(prefix + "Current platform is Linux/Unix.")
                lsh_file = os.getcwd() + "/launch.sh"
                cmd_args = f'{str(configuration.optimized_start)}'

                if os.path.exists(lsh_file) and os.path.getsize(lsh_file) > 0:
                    pass

                else:
                    print(prefix + "Launch.sh script not found. Generating...", end="")
                    os.system("touch launch.sh")
                    with open("launch.sh", "a") as launch_file:
                        launch_file.write('#!/bin/sh\ncd \"$(dirname \"$(readlink -fn \"$0\")\")\"' + "\n" + cmd_args)
                    print("Done.")

                cmd_args = "bash launch.sh"

            else:
                print(prefix + "Unsupported OS: '" + platform.system() + "'!")
                print(prefix + "Exiting...")
                time.sleep(1)
                exit()

            print("\n" + prefix + "Starting server with the most efficient configuration...\n" + prefix, end="")
            os.system(cmd_args)
            time.sleep(3)
            clear_screen()

        # Settings
        elif user_input == '2':
            clear_screen()
            print("!-[Settings]-!\n\nAllocated Ram: " + configuration.ram + "GB\n\n"
                  "[1] Delete config\n"
                  "[2] Configure auto-start\n"
                  "[3] Change ram size\n"
                  "[4] Accept EULA agreement\n"
                  "[5] Return to menu\n")

            while True:
                user_input = input(prefix)

                if user_input == "1":
                    print(prefix + "Deleting configuration...", end="")
                    os.remove("user_config.ini")
                    print("Done!\n" + prefix + "Restarting...")
                    time.sleep(0.75)
                    clear_screen()
                    configuration()
                    break

                elif user_input == "2":
                    config.read('user_config.ini')

                    if auto_start_status == 'true':
                        print(prefix + "Current status is True. Would you like to disable? (Y)es/(N)o ")
                        user_input = input(prefix)

                        if user_input.lower() in yes_array:
                            config['Server Settings']['Auto Start'] = 'false'
                            with open("user_config.ini", "w+") as configfile:
                                config.write(configfile)
                            config.close()
                            print(prefix + "Auto-start is set to False.\n")
                        else:
                            print()

                    elif auto_start_status == 'false':
                        print(prefix + "Current status is False. Would you like to enable? (Y)es/(N)o ")
                        user_input = input(prefix)

                        if user_input.lower() in yes_array:
                            config['Server Settings']['Auto Start'] = 'true'
                            with open("user_config.ini", "w+") as configfile:
                                config.write(configfile)
                            config.close()
                            print(prefix + "Auto-start is set to True.\n")
                        else:
                            print()

                elif user_input == "3":
                    config.read('user_config.ini')

                    print(prefix + "Enter your newly desired ram value in GB. ")
                    user_input = input(prefix)

                    config['Server Settings']['Allocated Ram'] = user_input
                    with open("user_config.ini", "w+") as configfile:
                        config.write(configfile)

                    print(prefix + "New ram value is set to " + user_input + "GB\n")
                    print(prefix + "Reloading configuration file...")
                    configuration()
                    print(prefix + "Reload complete.\n")

                elif user_input == "4":
                    print(prefix + "Opening eula.txt...", end="")
                    with open("eula.txt", "w+") as eula_file:
                        print("Done.")
                        print(prefix + "Accepting eula agreement...", end="")
                        eula_file.write('eula=true')
                        print("Done.\n")

                elif user_input == "5":
                    clear_screen()
                    break

                else:
                    clear_screen()
                    print("!-[Settings]-!\n\nAllocated Ram: " + configuration.ram + "GB\n\n1. Delete config\n"
                                                                                    "2. Return to menu\n")
                    continue

        # Jar Downloader
        elif user_input == "3":
            clear_screen()
            config.read('user_config.ini')
            print("!-[Server Jar Manager]-!\n\nPaper is the best server software in terms of performance. \n\n"
                  "All Paper versions: ", end="")
            get_server_jar_versions()

            while True:
                print("\n" + prefix + "Enter your desired server version, or simply type exit to return to the main "
                                      "menu.")
                user_input = input(prefix)
                if user_input == "exit":
                    clear_screen()
                    break
                else:
                    config.read("user_config.ini")
                    latest_build = get_latest_build_version(user_input)
                    print("\n" + prefix + "Server version: " + user_input + " Selected.")
                    print(prefix + "Latest build for Server version: " + user_input + " is " + latest_build)

                    if latest_build <= config['Server Settings']['Paper Version']:
                        print(prefix + "Your current build is the latest build. (Current: " +
                              config['Server Settings']['Paper Version'] + "| Latest: " + latest_build + ")")
                        print(prefix + "No action required, you're running the latest build.")
                        print(prefix + "Returning to main menu in 5 seconds...")
                        time.sleep(5)
                        clear_screen()
                        break
                    else:
                        print(prefix + "Appending build version to config file...", end="")

                        config['Server Settings']['Paper Version'] = latest_build
                        with open("user_config.ini", "w+") as configfile:
                            config.write(configfile)
                        print("Done!")

                        print(prefix + "Connecting to papermc.io to download jar file...\n")
                        get_paper(user_input)
                        print("\n" + prefix + "Jar downloaded successfully!")
                        print(prefix + "Looking for existing eula.txt...", end="")

                        if glob.glob("eula.txt"):
                            print("[OK]")
                            print(prefix + "Returning to main menu in 5 seconds...")
                            time.sleep(5)
                            clear_screen()
                            break
                        else:
                            print("[Not Found]")

                            print(prefix + "Starting server to generate eula.txt\n")
                            os.system("java -Xms2G -Xmx2G -jar server.jar")

                            print("\n" + prefix + "Eula.txt generated.")
                            print(prefix + "Automatically open eula.txt to accept eula agreement? (Y/n)")

                            user_input = input(prefix)

                            if user_input.lower() in yes_array:
                                print(prefix + "Opening eula.txt...", end="")
                                with open("eula.txt", "w+") as eula_file:
                                    print("Done.")
                                    print(prefix + "Accepting eula agreement...", end="")
                                    eula_file.write('eula=true')
                                    print("Done.")

                                print(prefix + "Eula agreement acceptance complete.")
                                print(prefix + "Returning to main menu in 5 seconds...")
                                time.sleep(5)
                                clear_screen()
                                break
                            else:
                                print(prefix + "Eula agreement required for server to start.")
                                print(prefix + "Returning to main menu in 5 seconds...")
                                time.sleep(5)
                                clear_screen()
                                break

        # Exit program
        elif user_input == '4':
            print(prefix + "Exiting...")
            time.sleep(0.75)
            exit()

        else:
            clear_screen()


if __name__ == '__main__':
    main()
