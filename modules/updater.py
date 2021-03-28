import urllib.request

vf = open("./modules/version.txt", "r")
__version__ = (vf.read()).strip()

master_version = urllib.request.urlopen()
