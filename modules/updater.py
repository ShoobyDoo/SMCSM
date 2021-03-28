import urllib.request

global master_version
vf = open("./modules/version.txt", "r")
__version__ = (vf.read()).strip()


def get_latest_version():
    master_version_raw = urllib.request.urlopen("https://raw.githubusercontent.com/Doomlad/SMCSM/master/modules/version.txt")
    master_version = master_version_raw.read().decode('utf-8')

    return master_version


def is_latest():
    curr_ver = "1.0.9-pre12"
    test = curr_ver.split("-pre")

    print(get_latest_version())
    print(test[0].strip(), "\n", test[1].strip())
    # if version_checker(str())


print((1, 0, 9, 13) > (1, 0, 9, 12))
is_latest()