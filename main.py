''' Executes all scripts '''
import os

if __name__ == "__main__":
    os.system("python3 " + "setup.py")
    os.system("python3 " + "startStaging.py")
    os.system("python3 " + "downloadDataproducts.py")
