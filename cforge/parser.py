import ast

class Parser():
    def __init__(self,source:str):
        """
Gets input configuration source code
        """
        self.source=source.strip().splitlines()
        self.line=self.source[0]
        self.linepos=0
        self.res=[
            {
            "project": {}
            }
        ]

    def advance(self)->str:
        """
Goto next line
        """
        self.linepos+=1
        if (self.linepos<len(self.source)):
            self.line=self.source[self.linepos]
        return self.line

    def parse(self)->dict:
        """
Actual Parser that checks for statements
        """
        self.source.append(None)
        while (self.line != None):
            if self.line.startswith("import"):
                self.parse_import()
            elif self.line.startswith("project."):
                self.parse_project()
            else:
                self.parse_common()
            self.advance()
        return self.res

    def parse_import(self)->None:
        """
Parsing importing libs
        """
        self.res.append({
        "mod": "import",
        "val": ' '.join(self.line.split(" ")[1:]).strip()
        })
    
    def parse_project(self)->None:
        """
Parser project arguments
        """
        self.res[0]["project"][
            self.line.split(".")[1].split("=")[0].strip()
        ]='='.join(self.line.split("=")[1:]).strip()[1:-1]
    
    def parse_common(self) -> None:
        """
Parse python-like variables
        """
        if self.line == '':
            return None
        checking = True
        bracket = False
        count = 0
        res = ""
        while (self.line != None and checking):
            if ('{' in self.line):
                bracket = False
                checking = False
                count += 1
            elif ('[' in self.line):
                bracket = True
                checking = False
                count += 1                
            res += self.line
        if (']' in self.line and bracket): count-=1; res=self.line
        if ('}' in self.line and not bracket): count-=1; res=self.line
        self.advance()
        while (self.line != None and count != 0):
            if ('{' in self.line and not bracket):
                count += 1
            if ('[' in self.line and bracket):
                count += 1
            if ("}" in self.line and not bracket):
                count -= 1
            if ("]" in self.line and bracket):
                count -= 1
            res += self.line.strip()
            self.advance()
        par = ast.parse(res)
        if isinstance(par.body[0].targets[0], ast.Name):
            var_name = str(par.body[0].targets[0].id)
        elif isinstance(par.body[0].targets[0], ast.Attribute):
            var_name = str(par.body[0].targets[0].attr)
        else:
            raise TypeError("Invalid target type: {}".format(type(targets)))
        var_value = ast.literal_eval(par.body[0].value)
        self.res.append({"mod": "common", var_name: var_value})