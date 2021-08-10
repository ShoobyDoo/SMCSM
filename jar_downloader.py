import os
import urllib.request
import json


class JarDownloader:
    PAPER = 'paper'
    PAPER_API = 'https://papermc.io/api/v1/paper/'

    PURPUR = 'purpur'
    

    FORGE = 'forge'
    FORGE_API = 

    VANILLA = 'vanilla'



    def __init__(self, mc_version=None, jar_type=PAPER):
        self.mc_version = mc_version
        self.jar_type = jar_type
        self.server_jars = []

    def get_server_jar(self):
        if self.jar_type == 'papermc':
            os.system("curl https://papermc.io/api/v1/paper/" + self.mc_version + "/latest/download --output server.jar")
        else:
            print("CRITICAL: Unsupported server type")

    def get_latest_build_version(self):
        try:
            with urllib.request.urlopen("https://papermc.io/api/v1/paper/" + self.mc_version + r"/latest/") as url:
                data = json.loads(url.read().decode("utf-8"))
                build = data['build']
                return build
        except:
            return "ERROR: Could not retrieve latest build for requested version: " + self.mc_version


    def get_server_jar_versions(self):
        if self.jar_type == self.PAPER:
            self.server_jars = []
            with urllib.request.urlopen("https://papermc.io/api/v1/paper/") as url:
                data = json.loads(url.read().decode("utf-8"))
        
        counter = 0
        for versions in data['versions']:
            self.server_jars.append(versions)
            if counter == 6:
                print(end="\b\n                     ")
                counter = 0
            print(versions, end=", ")
            counter += 1
        print("\b\b")


def main():
    smcjd = JarDownloader()
    smcjd.get_server_jar_versions()


main()
