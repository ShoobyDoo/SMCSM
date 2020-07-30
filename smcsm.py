# Simple Minecraft Server Manager
# By Doomlad
# 07/01/2020

# <--------------[Imports]----------------> #
import subprocess
from subprocess import Popen, PIPE
from modules.config_gen import *
from modules.menu import *
from modules.clear_screen import *
from modules.jar_downloader import *
from modules.prerequisites import *

try:
    import yaml
    from progress.bar import Bar
    from modules.server_backups import *
    from modules.server_optimizer import *
except ModuleNotFoundError:
    pass
# <--------------[Imports]----------------> #

prefix = "[SMCSM] » "
yes_array = ['y', 'yes']


# Main function
def main():
    global server
    # Clear screen at program start
    clear_screen()

    # Smarter dependencies check
    dependencies = ["PyYAML", "progress", "mctools[color]"]
    print(prefix + "Looking for ", end="")
    for depend in dependencies:
        prerequisites(depend)
        if depend == dependencies[-1]:
            print(": [OK]\n")
        else:
            print(": [OK]", end=", ")

    # Call configuration function (Check for config file)
    configuration()

    # TODO: Implement some sort of version checker against config file ???
    # check_server_version()

    # Main while-loop to handle menu
    while True:
        menu()  # Call menu function (Prints menu)
        config = configparser.ConfigParser()
        config.read('user_config.ini')  # Read user config file
        auto_start_status = config['Server Settings']['Auto Start']  # Extract the auto-start condition

        # If auto-start condition is true, start program in 3 seconds
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

            # If user presses CTRL+C (KeyboardInterrupt), break out of auto-start
            except KeyboardInterrupt:
                user_input = input("\n" + prefix)
                pass

        # If not, print input prompt and await user entry
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

            def settings_items():
                try:
                    config = configparser.ConfigParser()
                    config.read('user_config.ini')
                    with open("eula.txt", "r") as eula_file:
                        content = eula_file.readline()
                        if content == "eula=false":
                            eula = "false"
                        elif content == "eula=true":
                            eula = "true"
                    eula_file.close()
                except Exception:
                    eula = "ERROR READING EULA"

                settings_items.counter = 0
                settings_items.settings_menu_items = [
                    "Delete config",
                    "Configure auto-start  | Current: " + config['Server Settings']['Auto Start'],
                    "Change ram size       | Current: " + config['Server Settings']['Allocated Ram'] + "GB",
                    "Accept EULA agreement | Current: " + eula,
                    "Server Optimization",
                    "Return to menu"
                ]

                # Settings menu
                settings_items.settings_banner = "!-[Settings]-!\n"
                print(settings_items.settings_banner)
                for item in settings_items.settings_menu_items:
                    settings_items.counter += 1
                    print("[" + str(settings_items.counter) + "] » " + item)
                print()

            settings_items()

            # Menu item selection
            while True:
                user_input = input(prefix)

                # =========================== #
                # [ Option 1: Delete config ] #
                # =========================== #
                if user_input == "1":
                    print(prefix + "Deleting configuration...", end="")
                    os.remove('user_config.ini')
                    print("Done!\n" + prefix + "Restarting...")
                    time.sleep(0.75)
                    configuration()
                    clear_screen()
                    break

                # ================================== #
                # [ Option 2: Configure auto-start ] #
                # ================================== #
                elif user_input == "2":
                    config = configparser.ConfigParser()
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

                # ================================================= #
                # [ Option 3: Change ram size (ram configuration) ] #
                # ================================================= #
                elif user_input == "3":
                    config = configparser.ConfigParser()
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

                # ================================ #
                # [ Option 4: Accept EULA option ] #
                # ================================ #
                elif user_input == "4":
                    print(prefix + "Opening eula.txt...", end="")
                    with open("eula.txt", "w+") as eula_file:
                        print("Done.")
                        print(prefix + "Accepting eula agreement...", end="")
                        eula_file.write('eula=true')
                        print("Done.\n")
                        eula_file.close()

                # ================================= #
                # [ Option 5: Server Optimization ] #
                # ================================= #
                elif user_input == "5":
                    server_opt()
                    input("\n" + prefix + "Press [ENTER] to return to the main menu.")
                    # print(prefix + "Returning to main menu in 5 seconds...")
                    # time.sleep(5)
                    clear_screen()
                    break

                # [ Last Option: Exit to Main Menu ] #
                elif user_input == str(len(settings_items.settings_menu_items)):
                    clear_screen()
                    break

                else:
                    clear_screen()
                    settings_items()
                    continue

        # [ Option 3: Jar Downloader ] #
        elif user_input == "3":
            clear_screen()
            config = configparser.ConfigParser()
            config.read('user_config.ini')
            print("!-[Server Jar Manager]-!\n\nPaper is the best server software in terms of performance. \n\n"
                  "All Paper versions: [", end="")
            get_server_jar_versions()

            while True:
                print("\n" + prefix + "Enter your desired server version, or simply type exit to return to the main "
                                      "menu.")
                user_input = input(prefix)
                if user_input == "exit":
                    clear_screen()
                    break

                elif user_input in get_server_jar_versions.paper_jars:
                    config = configparser.ConfigParser()
                    config.read("user_config.ini")
                    latest_build = get_latest_build_version(user_input)
                    print("\n" + prefix + "Server version: " + user_input + " Selected.")
                    print(prefix + "Latest build for Server version: " + user_input + " is " + latest_build)

                    try:
                        if latest_build <= config['Server Settings'][user_input]:
                            print(prefix + "Your current build is the latest build. [Current: " +
                                  config['Server Settings'][user_input] + " | Latest: " + latest_build + "]")
                            print(prefix + "No action required, you're running the latest build.")

                            counter = 5
                            print("\n" + prefix + "Press [CTRL + C] to bypass and download anyways. Exiting in: ",
                                  end="", flush=True)
                            for i in range(counter):
                                print(counter, end="\b", flush=True)
                                counter -= 1
                                time.sleep(1)

                            print("Times up! Exiting...", end="\b", flush=True)
                            print()

                            clear_screen()
                            break

                        else:
                            print(prefix + "Appending build version to config file...", end="")

                            config['Server Settings'][user_input] = latest_build
                            with open("user_config.ini", "w+") as configfile:
                                config.write(configfile)
                            print("Done!")

                            print(prefix + "Connecting to papermc.io to download jar file...\n")
                            get_paper(user_input)
                            print("\n" + prefix + "Jar downloaded successfully!")
                            print(prefix + "Looking for existing eula.txt...", end="")

                            if glob.glob("eula.txt"):
                                print("[OK]")

                                # ONCE EULA AGREEMENT IS ACCEPTED, START SERVER ONCE TO GENERATE FILES #
                                print(prefix + "Starting server for the first time to generate data...")

                                try:
                                    server = Popen(["java -Xms2G -Xmx2G -jar server.jar nogui"], stdin=PIPE,
                                                   stdout=PIPE)
                                    server.communicate(input='stop\n'.encode())
                                    server.kill()

                                except:
                                    debug = Popen(["java", "-Xms2G", "-Xmx2G", "-jar", "server.jar", "nogui"],
                                                  stdin=PIPE,
                                                  stdout=PIPE)
                                    debug.communicate(input="stop\n".encode())
                                    debug.kill()

                                clear_screen()
                                break

                            else:
                                print("[Not Found]")

                                print(prefix + "Starting server to generate eula.txt\n")
                                os.system("java -Xms2G -Xmx2G -jar server.jar nogui")

                                print("\n" + prefix + "Eula.txt generated.")

                                user_input = "yes"

                                if user_input.lower() in yes_array:
                                    print(prefix + "Opening eula.txt...", end="")
                                    with open("eula.txt", "w+") as eula_file:
                                        print("Done.")
                                        print(prefix + "Accepting eula agreement...", end="")
                                        eula_file.write('eula=true')
                                        print("Done.")

                                    print(prefix + "Eula agreement acceptance complete.\n")

                                    # ONCE EULA AGREEMENT IS ACCEPTED, START SERVER ONCE TO GENERATE FILES #
                                    print(prefix + "Starting server for the first time to generate data...")

                                    try:
                                        server = Popen(["java -Xms2G -Xmx2G -jar server.jar nogui"], stdin=PIPE,
                                                       stdout=PIPE)
                                        server.communicate(input='stop\n'.encode())
                                        server.kill()

                                    except:
                                        debug = Popen(["java", "-Xms2G", "-Xmx2G", "-jar", "server.jar", "nogui"],
                                                      stdin=PIPE,
                                                      stdout=PIPE)
                                        debug.communicate(input="stop\n".encode())
                                        debug.kill()

                                    clear_screen()
                                    break

                    except KeyboardInterrupt:
                        print()
                        print(prefix + "Appending build version to config file...", end="")

                        config['Server Settings'][user_input] = latest_build
                        with open("user_config.ini", "w+") as configfile:
                            config.write(configfile)
                        print("Done!")

                        print(prefix + "Connecting to papermc.io to download jar file...\n")
                        get_paper(user_input)
                        print("\n" + prefix + "Jar downloaded successfully!")
                        print(prefix + "Looking for existing eula.txt...", end="")

                        if glob.glob("eula.txt"):
                            print("[OK]")

                            # ONCE EULA AGREEMENT IS ACCEPTED, START SERVER ONCE TO GENERATE FILES #
                            print(prefix + "Starting server for the first time to generate data...\n")

                            try:
                                server = Popen(["java -Xms2G -Xmx2G -jar server.jar nogui"], stdin=PIPE, stdout=PIPE)
                                server.communicate(input='stop\n'.encode())
                                server.kill()

                            except:
                                debug = Popen(["java", "-Xms2G", "-Xmx2G", "-jar", "server.jar", "nogui"], stdin=PIPE,
                                              stdout=PIPE)
                                debug.communicate(input="stop\n".encode())
                                debug.kill()

                            clear_screen()
                            break

                        else:
                            print("[Not Found]")

                            print(prefix + "Starting server to generate eula.txt\n")
                            os.system("java -Xms2G -Xmx2G -jar server.jar")

                            print("\n" + prefix + "Eula.txt generated.")

                            user_input = "yes"

                            if user_input.lower() in yes_array:
                                print(prefix + "Opening eula.txt...", end="")
                                with open("eula.txt", "w+") as eula_file:
                                    print("Done.")
                                    print(prefix + "Accepting eula agreement...", end="")
                                    eula_file.write('eula=true')
                                    print("Done.")

                                print(prefix + "Eula agreement acceptance complete.\n")

                                # ONCE EULA AGREEMENT IS ACCEPTED, START SERVER ONCE TO GENERATE FILES #
                                print(prefix + "Starting server for the first time to generate data...\n")

                                try:
                                    server = Popen(["java -Xms2G -Xmx2G -jar server.jar nogui"], stdin=PIPE,
                                                   stdout=PIPE)
                                    server.communicate(input='stop\n'.encode())
                                    server.kill()

                                except:
                                    debug = Popen(["java", "-Xms2G", "-Xmx2G", "-jar", "server.jar", "nogui"],
                                                  stdin=PIPE,
                                                  stdout=PIPE)
                                    debug.communicate(input="stop\n".encode())
                                    debug.kill()

                                clear_screen()
                                break

        # [ Option 4: Backup Manager ] #
        elif user_input == '4':

            while True:
                clear_screen()
                config = configparser.ConfigParser()
                config.read('user_config.ini')
                backup_banner = "!-[Backup Manager]-!\n\n" \
                                "Keep track of and setup (automatic backups + install updates COMING SOON...1.0.9)\n"
                print(backup_banner)

                bm_items = ["Create a backup", "Existing backups", "Return to menu"]

                counter = 0
                for items in bm_items:
                    counter += 1
                    print("[" + str(counter) + "] » " + items)
                print()

                user_input = input(prefix)

                # DEBUG OPTION (OUTLINE FOR FILE DELETION WHEN INSTALLING BACKUPS) #
                if user_input == 'dsf':
                    delete_server_files(world_only=False)
                    input("ENTER")
                # DEBUG OPTION (OUTLINE FOR FILE DELETION WHEN INSTALLING BACKUPS) #

                if user_input == '1':
                    while True:
                        clear_screen()
                        print(backup_banner + "\n" +
                              "[1] » Full backup\n"
                              "[2] » Worlds only\n"
                              "[3] » Back to previous menu\n")
                        user_input = input(prefix)

                        if user_input == '1':
                            backup_manager(full_backup=True)
                            print(prefix + "Backup complete. Returning in 3 seconds...")
                            time.sleep(3)
                            break

                        elif user_input == "2":
                            backup_manager(full_backup=False)
                            print(prefix + "Backup complete. Returning in 3 seconds...")
                            time.sleep(3)
                            break

                        elif user_input == "3":
                            break

                        else:
                            continue

                elif user_input == '2':
                    while True:
                        clear_screen()
                        print(backup_banner)

                        backup_zips = []

                        # For dirs, sub-dirs, and files, search for .zips
                        for dir_path, dir_names, file_names in os.walk(os.getcwd()):
                            if "modules" in dir_names:
                                pass
                            for file_name in file_names:
                                if file_name.endswith(".zip"):
                                    backup_zips.append(file_name)

                        def existing_backups():
                            counter = 0
                            for zips in backup_zips:
                                counter += 1

                                if zips.startswith("(W) "):
                                    backup_type = r" | Type:[Worlds Only]"
                                elif zips.startswith("(F) "):
                                    backup_type = r" | Type:[Full Backup]"
                                else:
                                    backup_type = r" | Type:[Unrecognized Backup]"

                                # <----[Processing Date/Time]----> #
                                zip_data = zips.split("_")  # (1) 2020-07-28 | (2) PM7-08-24.zip
                                zip_date = zip_data[1].split("-")  # (0) 2020 year | (1) 07 month | (2) 28 day

                                zip_time = zip_data[2].split(".zip")  # zip_time[1] = PM7-08-24
                                zip_time = zip_time[0].split("-")
                                # <----[Processing Date/Time]----> #

                                # <----[Formatted Date]----> #
                                zip_year = zip_date[0]
                                zip_month = zip_date[1]
                                zip_day = zip_date[2]
                                # <----[Formatted Date]----> #

                                # <----[Formatted Time]----> #
                                zip_time_period = zip_time[0]
                                zip_hour = zip_time[1]
                                zip_minute = zip_time[2]
                                zip_second = zip_time[3]
                                # <----[Formatted Time]----> #

                                if zip_month == "01":
                                    zip_month = "January"
                                elif zip_month == "02":
                                    zip_month = "February"
                                elif zip_month == "03":
                                    zip_month = "March"
                                elif zip_month == "04":
                                    zip_month = "April"
                                elif zip_month == "05":
                                    zip_month = "May"
                                elif zip_month == "06":
                                    zip_month = "June"
                                elif zip_month == "07":
                                    zip_month = "July"
                                elif zip_month == "08":
                                    zip_month = "August"
                                elif zip_month == "09":
                                    zip_month = "September"
                                elif zip_month == "10":
                                    zip_month = "October"
                                elif zip_month == "11":
                                    zip_month = "November"
                                elif zip_month == "12":
                                    zip_month = "December"

                                zip_metadata = f" | Date:[{zip_month} {zip_day}, {zip_year}]" \
                                               f" | Time:[{zip_hour}:{zip_minute} {zip_time_period}]"

                                if zips == backup_zips[len(backup_zips) - 1]:
                                    print("[" + str(counter) + "] » " + zips + backup_type + zip_metadata + " (Latest)")
                                else:
                                    print("[" + str(counter) + "] » " + zips + backup_type + zip_metadata)

                            print()

                            if len(backup_zips) == 0:
                                print("[!] » No backup zips were found.\n")
                            print(f"[{len(backup_zips) + 1}] » Back to previous menu")

                        existing_backups()
                        print()

                        try:
                            while True:
                                user_input = input(prefix)
                                clear_screen()

                                zip_selected = backup_zips[int(user_input) - 1]

                                while True:
                                    clear_screen()
                                    print(backup_banner)

                                    print(f"You selected: {zip_selected}\n\n"
                                          "[1] » Install backup\n"
                                          "[2] » Delete backup\n"
                                          "[3] » Back to previous menu\n")

                                    user_input = input(prefix)

                                    if user_input == "1":
                                        input("INCOMPLETE FEATURE. FINISHED IN 1.0.9, STAY TUNED (PRESS ENTER)")
                                        pass
                                        # TODO: INSTALL UPDATE BASED ON FULL/WORLD

                                    elif user_input == "2":
                                        print(prefix + "Are you sure you want to delete this backup? (y/N)")
                                        user_input = input(prefix)
                                        if user_input.lower() == "y":
                                            print(prefix + "Deleting...", end="")
                                            os.remove(zip_selected)
                                            print("Done!")
                                            print(prefix + "Returning to previous menu in 3 seconds...")
                                            time.sleep(3)
                                            break

                                        else:
                                            continue

                                    elif user_input == "3":
                                        break

                                    else:
                                        continue

                                break

                        except IndexError:
                            break

                        except ValueError:
                            continue

                # Access last item in Array (Always going to be Return to menu)
                elif user_input == str(len(bm_items)):
                    break

                else:
                    continue

            clear_screen()

        # [ Last Option: Exit program ] #
        elif user_input == str(len(menu.menu_items)):
            print(prefix + "Exiting...")
            time.sleep(0.75)
            exit()

        else:
            clear_screen()


if __name__ == '__main__':
    main()
