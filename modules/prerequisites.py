# Simple Minecraft Server Manager
# By Doomlad
# 07/14/2020

from setuptools.command.easy_install import main as install
import time
import os
import platform


def prerequisites(package):
    if platform.system() == "Windows":
        os.system("cls")
    elif platform.system() == "Linux" or platform.system() == "Darwin":
        os.system("clear")

    print(f"[SMCSM] » Looking for {package}.......", end="")
    while True:
        try:
            if package == 'PyYAML':
                package = 'yaml'

            return __import__(package)

        except ImportError:
            print("[NO]\n")
            if package == 'yaml':
                package = 'PyYAML'

            print("You are missing the module " + package + "\n(Install once and forget about it)")
            user_input = input("\nWould you like to install it? y/n: ")

            if user_input == 'y':
                print("Installing " + package + " via pip...", end="")
                install([package])
                print("Done!\nPlease restart the program.")
                counter = 4
                for count in range(3):
                    counter -= 1
                    print("Exiting in..." + str(counter), end="\r")
                    time.sleep(1)
                break

            elif user_input == 'n':
                print("\nThis program cannot function without " + package + ", please consider installing to continue."
                                                                            "\n")
                counter = 4
                for count in range(3):
                    counter -= 1
                    print("Exiting in..." + str(counter), end="\r")
                    time.sleep(1)
                break
        exit()
