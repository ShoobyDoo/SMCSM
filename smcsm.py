# Simple Minecraft Server Manager
# By Doomlad
# 07/01/2020

import os
import configparser
import time
import platform
from modules.config_gen import configuration
from modules.menu import menu
from modules.clear_screen import clear_screen

prefix = "[SMCSM] » "
config = configparser.ConfigParser()
yes_array = ['y', 'yes']
no_array = ['n', 'no']


def main():
    configuration()
    while True:
        menu()
        config.read('user_config.ini')
        auto_start_status = config['Server Settings']['Auto Start']

        if auto_start_status == 'true':
            user_input = '1'

            try:
                print("\n" + prefix + "Press [CTRL + C] to bypass auto-start. Starting in 3 seconds...")
                for i in range(3):
                    time.sleep(1)

            except KeyboardInterrupt:
                user_input = input("\n" + prefix)
                pass

        else:
            user_input = input("\n" + prefix)

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
                    print(prefix + "Launch.sh script not found. Generating...")
                    os.system("touch launch.sh")
                    with open("launch.sh", "a") as launch_file:
                        launch_file.write('#!/bin/sh\ncd \"$(dirname \"$(readlink -fn \"$0\")\")\"' + "\n" + cmd_args)

                cmd_args = "bash launch.sh"

            else:
                print(prefix + "Unsupported OS: '" + platform.system() + "'!")
                print(prefix + "Exiting...")
                time.sleep(1)
                exit()

            print("\n" + prefix + "Starting server with the most efficient configuration...")
            os.system(cmd_args)
            input("\n" + prefix + "Press enter to continue.")
            clear_screen()

        elif user_input == '2':
            clear_screen()
            print("!-[Settings]-!\n\nAllocated Ram: " + configuration.ram + "GB\n\n"
                  "[1] Reset config\n"
                  "[2] Configure auto-start\n"
                  "[3] Return to menu\n")

            while True:
                user_input = input(prefix)

                if user_input == "1":
                    print(prefix + "Resetting configuration...", end="")
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

                elif user_input == "3":
                    clear_screen()
                    break

                else:
                    clear_screen()
                    print("!-[Settings]-!\n\nAllocated Ram: " + configuration.ram + "GB\n\n1. Delete config\n"
                                                                                    "2. Return to menu\n")
                    continue

        elif user_input == '3':
            print(prefix + "Exiting...")
            time.sleep(0.50)
            exit()

        else:
            clear_screen()


if __name__ == '__main__':
    main()
