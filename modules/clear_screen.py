# Simple Minecraft Server Manager
# By Doomlad
# 07/01/2020

import os
import platform


def clear_screen():

    if platform.system() == "Windows":
        os.system("cls")
    elif platform.system() == "Linux" or platform.system() == "Darwin":
        os.system("clear")
    else:
        print("Unsupported OS: '" + platform.system() + "'!")
