''' Executes all scripts '''
import os

from parsers._configparser import getConfigs

if __name__ == "__main__":
    os.system("python3 " + "startStaging2.py")
    if getConfigs("Operations", "Retrieve", "config.cfg") == "True":
        os.system("python3 " + "downloadDataproducts2.py")

    if getConfigs("Operations", "Process", "config.cfg") == "True":
        os.system("python3 " + "runPipelins.py")
