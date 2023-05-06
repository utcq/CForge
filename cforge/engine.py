from .checker import *
from os import system
from glob import glob
from re import findall

class Lang:
    CL="gcc"
    CPP="g++"

class Engine():
    def __init__(self, result:list[dict], root=""):
        """
No-Return class, Direct Execution 
        """
        self.command=[]
        self.result=result
        self.root=root
        self.arch=Checker.arch()
        self.run()

    def p_targets(self, files, excls)->str:
        all_files = []
        for target in files:
            all_files.extend(glob(self.root+"src/"+target))

        exclude_files = []
        for exclude in excls:
            exclude_files.extend(glob(exclude))

        return ' '.join(list(set(all_files) - set(exclude_files)))


    def p_lib(self, lname)->str:
        """
Parse library import and raise error if there isn't the lib 
        """
        res=Checker.lib(lname)
        if res: return f'-l{lname}'
        else: raise Exception("BLAH BVL")

    def parse(self)->list[str]:
        """
Turn the config ast to compiler arguments
        """
        exclude=[]
        args=[]
        for arg in self.result:
            if "project" in arg: 
                for par in arg['project']:
                    match par:
                        case "name": args.append(f"-o {self.root+'build/'+self.arch+'/'+arg['project'][par]}")
                        case _: pass
            else:
                match arg["mod"]:
                    case "import":   args.append(self.p_lib(arg["val"]))
                    case "common":
                        for part in arg:
                            match part:
                                case "exclude": exclude=arg[part]
                                case "targets": 
                                    args.append(self.p_targets(arg[part], exclude))
                                case "args":
                                    if arg[part] != []: args.append(' '.join(arg[part]))
                                case "dirs":
                                    for fold in arg[part]:
                                        args.append(f'-I src/{fold}')
                                    
                                case _: pass
                            
                    case _: pass
        return ' '.join(args)
    def run(self)->None:
        """
Actual execution engine
        """

        # -------------
        Checker.ecreate(self.root+"build/"+self.arch+"/")
        # -------------



        # -------------
        compiler=self.recognizer()
        self.command.append(compiler)
        # --------------



        # -------------
        args=self.parse()
        self.command.append(args)
        # -------------

        cmds=' '.join(self.command)
        print(cmds)
        system(cmds)


    def recognizer(self)->Lang:
        """
Check if the project uses C++ or C. And return the compiler command
        """
        c_files   = glob(self.root + 'src/*.c', recursive=True)
        cpp_files = glob(self.root + 'src/*.cpp', recursive=True)
        files     = c_files + cpp_files
        c_count = len(c_files)
        cpp_count = len(cpp_files)

        if (c_count > cpp_count): return Lang.CL
        else: return Lang.CPP