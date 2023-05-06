import cforge
import json

source=open("examples/cforge","r").read()
parser=cforge.Parser(source)
pz=parser.parse()
print(json.dumps(pz, indent=2))