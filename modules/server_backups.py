# Simple Minecraft Server Manager
# By Doomlad
# 07/15/2020

import os
import time
import zipfile
import shutil
import glob
from zipfile import ZipFile
from os.path import basename
from datetime import datetime
from progress.bar import ChargingBar

prefix = "[SMCSM] » "


def backup_manager(full_backup=False):
    start_time = time.perf_counter()
    now = datetime.now()

    current_hour = now.strftime("%H")
    current_minute = now.strftime("%M")
    current_second = now.strftime("%S")

    if int(current_hour) > 12:
        current_hour = "PM-" + str(int(current_hour) - 12)
    else:
        current_hour = "AM-" + str(int(current_hour) - 12)

    current_time = str(current_hour) + "-" + str(current_minute) + "-" + str(current_second)

    parent_dir = os.getcwd()
    if full_backup:
        zip_filename = "(F) " + basename(str(parent_dir)) + "_" + str(datetime.date(datetime.now())) + "_" + \
                       current_time + ".zip"
    else:
        zip_filename = "(W) " + basename(str(parent_dir)) + "_" + str(datetime.date(datetime.now())) + "_" + \
                       current_time + ".zip"

    print(prefix + "Warning: The SMCSM files will NOT be zipped.")
    print(prefix + "Zipping content of: " + parent_dir)
    print(prefix + "This might take a while. Please wait...\n")

    outZipFile = ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED)
    root_dir = os.path.basename(os.getcwd())

    if full_backup:
        if os.path.exists(os.getcwd()):
            counter = 0
            for dir_path, dir_names, file_names in os.walk(os.getcwd()):
                if "modules" in dir_names:
                    pass
                for file_name in file_names:
                    if file_name.endswith(".zip") or file_name.endswith(".py"):
                        pass
                    else:
                        counter += 1

            bar = ChargingBar(prefix + "Processing Files", max=counter)
            for dir_path, dir_names, file_names in os.walk(os.getcwd()):
                if "modules" in dir_names:
                    pass
                for file_name in file_names:
                    bar.next()
                    if file_name.endswith(".zip") or file_name.endswith(".py"):
                        pass
                    else:
                        file_path = os.path.join(dir_path, file_name)
                        parent_path = os.path.relpath(file_path, os.getcwd())
                        arc_name = os.path.join(root_dir, parent_path)

                        outZipFile.write(file_path, arc_name)

            bar.finish()

    else:

        non_world_dirs = [
            "modules",
            ".vscode",
            ".idea",
            "plugins",
            "logs",
            "jar",
            ".git",
            "cache"
        ]

        world_dirs = []
        # counter = 0
        for root, subdirs, files in os.walk(os.getcwd()):
            for folders in subdirs:
                if folders not in non_world_dirs:
                    world_dirs.append(folders)

        world_files = 0
        for world_dir in world_dirs:
            full_path = os.getcwd() + "\\" + world_dir
            for root, subdirs, files in os.walk(full_path):
                for file in files:
                    world_files += 1

        bar = ChargingBar(prefix + "Processing files", max=world_files)
        for world_dir in world_dirs:
            full_path = os.getcwd() + "\\" + world_dir
            for root, subdirs, files in os.walk(full_path):
                for file in files:
                    bar.next()
                    file_path = os.path.join(root, file)
                    parent_path = os.path.relpath(file_path, os.getcwd())
                    arc_name = os.path.join(root_dir, parent_path)

                    outZipFile.write(file_path, arc_name)

        bar.finish()

    outZipFile.close()
    end_time = time.perf_counter()

    print("\n" + prefix + f"Zip process took {end_time - start_time:0.2f} seconds to complete.")
    print(prefix + "Zip file name is formatted as such: Folder_YYYY-MM-DD_Time.zip")


def delete_server_files(world_only=True):
    if world_only:
        start_time = time.perf_counter()

        non_world_dirs = [
            "modules",
            ".vscode",
            ".idea",
            "plugins",
            "logs",
            "jar",
            ".git"
        ]

        counter = 0
        bar = ChargingBar(prefix + "Deleting files", max=3)
        for root, subdirs, files in os.walk(os.getcwd()):
            for folders in subdirs:
                if folders not in non_world_dirs:
                    if counter == 3:
                        break
                    counter += 1
                    shutil.rmtree(folders)

        bar.finish()
        end_time = time.perf_counter()

        print(f"File deletion took {end_time - start_time:0.2f} seconds to complete.")

    else:
        start_time = time.perf_counter()

        counter = 0
        for dir_path, dir_names, file_names in os.walk(os.getcwd()):
            if "modules" in dir_names:
                pass
            for file_name in file_names:
                if file_name.endswith(".zip") or file_name.endswith(".py"):
                    pass
                else:
                    counter += 1
        print()
        bar = ChargingBar(prefix + "Deleting files")
        for dir_path, dir_names, file_names in os.walk(os.getcwd()):
            for file_name in file_names:
                if file_name == ".console_history" or file_name.endswith(".txt") or file_name.endswith(".properties"):
                    os.remove(file_name)

                if 'modules' in dir_names:
                    dir_names.remove('modules')

                elif '.idea' in dir_names:
                    dir_names.remove('.idea')

                elif '.git' in dir_names:
                    dir_names.remove('.git')

                    for dirs in dir_names:
                        bar.next()
                        shutil.rmtree(dirs)

        bar.finish()
        end_time = time.perf_counter()
        print("\n" + prefix + f"File deletion took {end_time - start_time:0.2f} seconds to complete.\n")

        start_time = time.perf_counter()
        # SPAGHETTI CODE, BIG YIKES TO ANYONE READING THIS #
        if file_name.endswith('.py') or file_name.startswith('.git') or file_name.startswith('.idea') or \
                file_name.endswith('.ini') or file_name.endswith('.pyc') or file_name == 'LICENSE' or \
                file_name == 'README.md':
            file_names.remove(file_name)
        # SPAGHETTI CODE, BIG YIKES TO ANYONE READING THIS #

        fileList = glob.glob(os.getcwd() + "\\*")

        counter = 0
        for residual_file in fileList:
            if residual_file.endswith(".json") or residual_file.endswith(".jar") or residual_file.endswith(".yml"):
                counter += 1

        bar = ChargingBar(prefix + "Cleaning up", max=counter)
        for residual_file in fileList:
            if residual_file.endswith(".json") or residual_file.endswith(".jar") or residual_file.endswith(".yml"):
                bar.next()
                os.remove(residual_file)

        bar.finish()
        end_time = time.perf_counter()
        print("\n" + prefix + f"Clean up process took {end_time - start_time:0.2f} seconds to complete.")
        print()


def extract_backup():
    print("")
    user_input = input(prefix)
