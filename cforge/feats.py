class Templates:
    """
Commit on github to add a template
    """


    codes = {
        "base": """
project.name="Your_Project_Name"

targets=[
    "*.c*"
]""",
        "lua": """
project.name="Your_Project_Name"

targets=[
    "*.c*"
]

import lua
"""

    }

    def load(name:str):
        """
Given the template name, return the template config code
        """
        code=""
        if name in Templates.codes:
            code=Templates.codes[name]
        else:
            raise Exception(f"{name} template not found!")
        open("cforge", "w").write(code)