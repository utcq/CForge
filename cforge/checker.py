from os.path import exists
from os import makedirs
from os import environ, uname
from ctypes.util import find_library
from sys import platform

class Checker:
    def isPath(arg:str)->bool:
        """
Check if the given CLI argument is a path or a script
        """
        return exists(arg)

        
    def lib(lname:str)->bool:
        """
Check if the give library exists and it's installed
        """
        if find_library(lname): return True
        else: return False

    def arch()->str:
        """
Check machine architecture
        """
        if platform.startswith('linux'):
            machine = uname().machine
            return machine
        elif platform == 'win32':
            processor = environ['PROCESSOR_ARCHITECTURE']
            if (processor in ['x86', 'AMD64']):
                return "x86_64"
            else:
                return "ARM"
        else:
            return 

    def ecreate(path:str)->None:
        """
Create folder if it doesn't exist
        """
        if not exists(path):
            makedirs(path)