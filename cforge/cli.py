from sys import argv
from .checker import *
from .feats import *

class CLIP():
    def __init__(self):
        self.args=argv
        del self.args[0]

    def parse(self)->tuple:
        """
Self explainatory
        """
        path=""
        scripts=[]
        for arg in self.args:
            if arg.startswith("-T="):
                Templates.load(arg.split("=")[1])
                exit(0)
            ref=Checker.isPath(arg)
            if ref:
                path=arg
                print("Path Set to: "+arg)
            else:
                scripts.append(arg)
        if not path.endswith("/") and path != "": path+="/"
        return (path, scripts)