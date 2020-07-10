__version__ = '1.0.5'
from modules.config_gen import configuration


def menu():
    print("-----------------------------------\n" +
          "-=[Simple MCServer Manager " + __version__ + "]=-\n"
          "-----------------------------------\n\n"
          "A simple local minecraft server management tool.\n")
    menu.menu_items = ["Start Server (" + configuration.ram + "GB)", "Settings", "Exit"]
    menu_counter = 0
    for item in menu.menu_items:
        menu_counter += 1
        print("[" + str(menu_counter) + "] » " + item)
