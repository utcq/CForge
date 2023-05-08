import cforge


root,scripts=cforge.CLIP().parse()
source=open(root+"cforge","r").read()
parser=cforge.Parser(source)
pz=parser.parse()
cforge.Engine(pz, root)