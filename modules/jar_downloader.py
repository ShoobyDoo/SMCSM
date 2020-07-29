# Simple Minecraft Server Manager
# By Doomlad
# 07/01/2020

import urllib.request
import json
import os


def get_paper(mc_version):
    os.system("curl https://papermc.io/api/v1/paper/" + mc_version + "/latest/download --output server.jar")


def get_latest_build_version(mc_version):
    try:
        with urllib.request.urlopen("https://papermc.io/api/v1/paper/" + mc_version + r"/latest/") as url:
            data = json.loads(url.read().decode("utf-8"))
            build = data['build']
            return build
    except:
        return "ERROR: Could not retrieve latest build for requested version: " + mc_version


def get_server_jar_versions():
    get_server_jar_versions.paper_jars = []
    with urllib.request.urlopen("https://papermc.io/api/v1/paper/") as url:
        data = json.loads(url.read().decode("utf-8"))
    counter = 0
    for versions in data['versions']:
        get_server_jar_versions.paper_jars.append(versions)
        if counter == 6:
            print(end="\b\n                     ")
            counter = 0
        print(versions, end=", ")
        counter += 1
    print("\b\b]")


