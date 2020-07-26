# Simple Minecraft Server Manager
# By Doomlad
# 07/15/2020

import os
import time
import zipfile
import shutil
from zipfile import ZipFile
from os.path import basename
from datetime import datetime
from progress.bar import ChargingBar

prefix = "[SMCSM] » "


def backup_manager():
    start_time = time.perf_counter()
    now = datetime.now()

    current_hour = now.strftime("%H")
    current_minute = now.strftime("%M")
    current_second = now.strftime("%S")

    if int(current_hour) > 12:
        current_hour = int(current_hour) - 12

    current_time = str(current_hour) + "-" + str(current_minute) + "-" + str(current_second)

    parent_dir = os.getcwd()
    zip_filename = basename(str(parent_dir)) + "_" + str(datetime.date(datetime.now())) + "_" + current_time + ".zip"

    print(prefix + "Warning: The SMCSM files will NOT be zipped.")
    print(prefix + "Zipping content of: " + parent_dir)
    print(prefix + "This might take a while. Please wait...\n")

    if os.path.exists(os.getcwd()):
        outZipFile = ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED)
        root_dir = os.path.basename(os.getcwd())

        counter = 0
        for dir_path, dir_names, file_names in os.walk(os.getcwd()):
            if "modules" in dir_names:
                pass
            for file_name in file_names:
                if file_name.endswith(".zip") or file_name.endswith(".py"):
                    pass
                else:
                    counter += 1

        bar = ChargingBar("Processing Files", max=counter)
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

    outZipFile.close()
    end_time = time.perf_counter()

    print("\n" + prefix + f"Zip process took {end_time - start_time:0.2f} seconds to complete.")
    print(prefix + "Zip file name is formatted as such: Folder_YYYY-MM-DD_Time.zip")


def delete_server_files():
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

    bar = ChargingBar("Deleting files", max=counter)
    for dir_path, dir_names, file_names in os.walk(os.getcwd()):
        for file_name in file_names:
            if 'modules' in dir_names or '.idea' in dir_names or '.git' in dir_names:
                dir_names.remove('modules')
                dir_names.remove('.idea')
                dir_names.remove('.git')
                for dirs in dir_names:
                    print(prefix + "Cleaning up directories...")
                    shutil.rmtree(dirs)
            else:
                if file_name.endswith('.py') or file_name.startswith('.git') or file_name.startswith('.idea') or \
                        file_name.endswith('.ini') or file_name.endswith('.pyc') or file_name == 'LICENSE' or \
                        file_name == 'README.md':
                    print(prefix + "Okay | " + file_name)

                else:
                    bar.next()
                    os.remove(file_name)
                    print(prefix + "Deleted | " + dirs)

    bar.finish()
    end_time = time.perf_counter()

    print("\n" + prefix + f"File deletion took {end_time - start_time:0.2f} seconds to complete.")


def extract_backup():

    print("")
    user_input = input(prefix)