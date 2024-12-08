import os

from typing import List


def snake_to_camel(snake_str):
    """Converts a snake_case string to camelCase."""
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def convertDbDiagramToPython(ignoreTables: List[str]):
    tables = {}
    script_dir = os.path.dirname(__file__)
    with open(os.path.join(script_dir, "HTCNotes.txt"), "r") as file:
        content = file.read()

        for tableNote in content.split(";"):
            tableNote = tableNote.strip()
            if tableNote[0:2] != "**":
                continue
            tableNote = tableNote[2:]

            accessTableNameStart = tableNote.find("[") + 1
            accessTableNameEnd = tableNote.find("]")
            accessTableName = tableNote[accessTableNameStart:accessTableNameEnd]
            accessTableVarName = accessTableName.replace(" ", "_")
            
            if accessTableVarName in ignoreTables:
                continue

            remainingNote = tableNote[accessTableNameEnd + 1 :].strip()
            if remainingNote != "=> NULL":
                sqlTableNameStart = remainingNote.find("[") + 1
                sqlTableNameEnd = remainingNote.find(":")
                sqlTableName = remainingNote[sqlTableNameStart:sqlTableNameEnd].strip()
                if " " not in sqlTableName: 
                    currTableFilePath = os.path.join(script_dir, rf'..\src\tables\access\{accessTableVarName}.py')
                    if os.path.exists(currTableFilePath):
                        os.remove(currTableFilePath)
                    with open(currTableFilePath, 'w+') as f:
                        f.write(f"from ...imports import *\n")
                        f.write(f"\n")
                        f.write(f"def convert_{accessTableVarName}(conn : Connection):\n")
                        f.write(f"    {sqlTableName}Info = conn.accessGetTableInfo('htc{accessTableName[3:6]}', '{accessTableName}')\n")
                        f.write(f"    for row in {sqlTableName}Info:\n")
                        f.write(f"        pass")

convertDbDiagramToPython([
    'HTC000_G010_T010_Company_Info'
])
