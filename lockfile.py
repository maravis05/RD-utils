
#Tries to create a temporary lock file in the same directory as the script.
#If the temporary file (named "lockfile") exists, this code will exit the current script.
#This will ONLY work in Windows (Possibly Linux)

import os

cwd = os.getcwd()

try:
    os.open(cwd+"\\lockfile", os.O_CREAT | os.O_EXCL | os.O_TEMPORARY )
except FileExistsError:
    print ("This application is already running.\n")
    input ("Press [ENTER] to exit.")
    exit()
except PermissionError: input("Need permission to create lock file.")
except Exception as e: input(e)



