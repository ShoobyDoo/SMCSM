# Simple Minecraft Server Manager
# By Doomlad
# 07/15/2020

import os
import time
import zipfile
from zipfile import ZipFile
from os.path import basename
from datetime import datetime
from progress.bar import Bar


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

    print("[SMCSM] » Zipping content of: " + parent_dir)
    print("[SMCSM] » This might take a while. Please wait...\n")

    if os.path.exists(os.getcwd()):
        outZipFile = ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED)
        root_dir = os.path.basename(os.getcwd())

        counter = 0
        for dir_path, dir_names, file_names in os.walk(os.getcwd()):
            for file_name in file_names:
                counter += 1

        bar = Bar("[SMCSM] » Processing Files", max=counter)
        for dir_path, dir_names, file_names in os.walk(os.getcwd()):
            for file_name in file_names:
                bar.next()
                if file_name.endswith(".zip"):
                    pass
                else:
                    file_path = os.path.join(dir_path, file_name)
                    parent_path = os.path.relpath(file_path, os.getcwd())
                    arc_name = os.path.join(root_dir, parent_path)

                    outZipFile.write(file_path, arc_name)

        bar.finish()

    outZipFile.close()
    end_time = time.perf_counter()

    print(f"\n[SMCSM] » Zip process took {end_time - start_time:0.2f} seconds to complete.")
    print("[SMCSM] » Zip file name is formatted as such: Folder_YYYY-MM-DD_Time.zip")
