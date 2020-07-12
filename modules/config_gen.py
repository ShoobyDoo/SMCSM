# Simple Minecraft Server Manager
# By Doomlad
# 07/01/2020

import configparser
import os
import time

prefix = "[SMCSM] » "


def configuration():
    while True:
        config = configparser.ConfigParser()
        try:
            # Search for config and if not found, prompt generation of first time configuration
            print(prefix + "Opening config file...", end="")
            if len(config.read('user_config.ini')) == 0:
                print("Not found!\n" + prefix + "Generating first time configuration...\n")
                configfile = open("user_config.ini", "w+")
                configfile.write("# SMCSM Configuration File #\n\n")
                config.add_section('Server Settings')
                print(prefix + "Enter your desired ram allocation in GB. (Default is 2.0GB)")
                ram = input(prefix)
                if ram == "":
                    config.set('Server Settings', 'Allocated Ram', '2')
                else:
                    config.set('Server Settings', 'Allocated Ram', ram)

                print(prefix + "Disabled auto-start by default. To enable, go to settings.")

                config.set('Server Settings', 'Paper Version', '')
                config.set('Server Settings', 'Auto Start', 'false')
                ram = float(ram) * 1000
                ram = "{:.0f}".format(ram)
                optimized_start = f'java ' \
                                  f'-Xms{str(ram)}M ' \
                                  f'-Xmx{str(ram)}M ' \
                                  f'-XX:+UseG1GC ' \
                                  f'-XX:+ParallelRefProcEnabled ' \
                                  f'-XX:MaxGCPauseMillis=200 ' \
                                  f'-XX:+UnlockExperimentalVMOptions ' \
                                  f'-XX:+DisableExplicitGC ' \
                                  f'-XX:-OmitStackTraceInFastThrow ' \
                                  f'-XX:+AlwaysPreTouch ' \
                                  f'-XX:G1NewSizePercent=30 ' \
                                  f'-XX:G1MaxNewSizePercent=40 ' \
                                  f'-XX:G1HeapRegionSize=8M ' \
                                  f'-XX:G1ReservePercent=20 ' \
                                  f'-XX:G1HeapWastePercent=5 ' \
                                  f'-XX:G1MixedGCCountTarget=8 ' \
                                  f'-XX:InitiatingHeapOccupancyPercent=15 ' \
                                  f'-XX:G1MixedGCLiveThresholdPercent=90 ' \
                                  f'-XX:G1RSetUpdatingPauseTimePercent=5 ' \
                                  f'-XX:SurvivorRatio=32 ' \
                                  f'-XX:MaxTenuringThreshold=1 ' \
                                  f'-Dusing.aikars.flags=true ' \
                                  f'-Daikars.new.flags=true ' \
                                  f'-jar server.jar nogui'

                config.set('Server Settings', 'Launch Args', optimized_start)
                print(prefix + "Writing config...", end="")
                config.write(configfile)
                configfile.close()
                print("Done. \n" + prefix + "Refreshing...\n")
                continue

            else:
                print("Found!")
                configuration.ram = config['Server Settings']['Allocated Ram']
                configuration.optimized_start = config['Server Settings']['Launch Args']
                break

        except (KeyError, configparser.MissingSectionHeaderError):
            print(prefix + "KeyError: Could not grab configuration from file. "
                  f"Deleting broken config...", end="")
            os.remove("user_config.ini")
            print("Done!\n" + prefix + "Restarting...")
            time.sleep(0.75)
