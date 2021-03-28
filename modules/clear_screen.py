# [ Title       ] : Simple Minecraft Server Manager
# [ Author      ] : Doomlad
# [ File        ] : clear_screen.py
# [ Description ] : Helper function to clear terminal based on OS
# [ Date        ] : 07 / 01 / 2020

import os
import platform


def clear_screen():
    
    if platform.system() == "Windows":
        os.system("cls")

    elif platform.system() == "Linux" or platform.system() == "Darwin":
        os.system("clear")

    else:
        input("Unsupported OS: '" + platform.system() + "'! (Press enter to continue)")
