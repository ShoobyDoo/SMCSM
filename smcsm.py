# Simple Minecraft Server Manager
# By Doomlad
# 07/01/2020

import os
import configparser
import time
import glob
import platform

from modules.config_gen import configuration, check_server_version
from modules.menu import menu
from modules.clear_screen import clear_screen
from modules.jar_downloader import get_paper, get_latest_build_version, get_server_jar_versions
from modules.prerequisites import prerequisites

try:
    import yaml
    from progress.bar import Bar
    from modules.server_backups import backup_manager
    from modules.server_optimizer import server_opt
except ModuleNotFoundError:
    pass

prefix = "[SMCSM] » "
config = configparser.ConfigParser()
yes_array = ['y', 'yes']


def main():
    prerequisites("PyYAML")
    print("[OK]")
    prerequisites("progress")
    print("[OK]")
    configuration()
    check_server_version()
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

        # [ Option 1: Start the Server ] #
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
                print(prefix + "Exiting in 5 seconds...")
                time.sleep(5)
                exit()

            print("\n" + prefix + "Starting server with the most efficient configuration...\n")
            os.system(cmd_args)
            clear_screen()

        # [ Option 2: Settings ] #
        elif user_input == '2':
            clear_screen()

            # Print settings menu
            settings_banner = "!-[Settings]-!\n\nAllocated Ram: " + configuration.ram + "GB\n\n" \
                              "[1] Delete config\n" \
                              "[2] Configure auto-start\n" \
                              "[3] Change ram size\n" \
                              "[4] Accept EULA agreement\n" \
                              "[5] Server Optimization\n" \
                              "[6] Return to menu\n"
            print(settings_banner)

            # Menu item selection
            while True:
                user_input = input(prefix)

                # [ Option 1: Delete config ] #
                if user_input == "1":
                    print(prefix + "Deleting configuration...", end="")
                    os.remove("user_config.ini")
                    print("Done!\n" + prefix + "Restarting...")
                    time.sleep(0.75)
                    clear_screen()
                    configuration()
                    break

                # [ Option 2: Configure auto-start ] #
                elif user_input == "2":
                    config.read('user_config.ini')

                    if auto_start_status == 'true':
                        print(prefix + "Current status is True. Would you like to disable? (Y)es/(N)o ")
                        user_input = input(prefix)

                        if user_input.lower() in yes_array:
                            config['Server Settings']['Auto Start'] = 'false'
                            with open("user_config.ini", "w+") as configfile:
                                config.write(configfile)
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
                            print(prefix + "Auto-start is set to True.\n")
                        else:
                            print()

                # [ Option 3: Change ram size (ram configuration) ] #
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

                # [ Option 4: Accept EULA option ] #
                elif user_input == "4":
                    print(prefix + "Opening eula.txt...", end="")
                    with open("eula.txt", "w+") as eula_file:
                        print("Done.")
                        print(prefix + "Accepting eula agreement...", end="")
                        eula_file.write('eula=true')
                        print("Done.\n")

                # [ Option 5: Server Optimization ] #
                elif user_input == "5":
                    server_opt()
                    input("\n" + prefix + "Press [ENTER] to return to the main menu.")
                    # print(prefix + "Returning to main menu in 5 seconds...")
                    # time.sleep(5)
                    clear_screen()
                    break

                # [ Last Option: Exit to Main Menu ] #
                elif user_input == "6":
                    clear_screen()
                    break

                else:
                    clear_screen()
                    print(settings_banner)
                    continue

        # [ Option 3: Jar Downloader ] #
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
                        print(prefix + "Your current build is the latest build. [Current: " +
                              config['Server Settings']['Paper Version'] + " | Latest: " + latest_build + "]")
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

        # [ Option 4: Backup Manager ] #
        elif user_input == '4':

            while True:
                clear_screen()
                config.read('user_config.ini')
                backup_banner = "!-[Backup Manager]-!\n\n" \
                                "Keep track of and setup automatic backups.\n"
                print(backup_banner)

                bm_items = ["Create full backup", "Return to menu"]

                counter = 0
                for items in bm_items:
                    counter += 1
                    print("[" + str(counter) + "] " + items)
                print()

                user_input = input(prefix)
                if user_input == '1':
                    backup_manager()
                    input("\n" + prefix + "Press [ENTER] to continue.")
                    continue

                elif user_input == '2':
                    break

                else:
                    continue

            # print(prefix + "Returning to main menu in 5 seconds...")
            # time.sleep(5)
            clear_screen()

        # [ Last Option: Exit program ] #
        elif user_input == '5':
            print(prefix + "Exiting...")
            time.sleep(0.75)
            exit()

        else:
            clear_screen()

        
if __name__ == '__main__':
    main()
