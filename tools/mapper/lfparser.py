import common
import configparser

def buildSection(names, nameToIdMap):
    s = ""

    lines = []

    for name in names:
        lines.append((str(nameToIdMap[name]) + ",").ljust(15) + "# " + name)

    return "\n        ".join(lines)

lflist = configparser.ConfigParser(allow_no_value=True, comment_prefixes=None)
lflist.read("lfinput.txt")

print(lflist["banned"])

names = []

for section in lflist.sections():
    for name in lflist[section]:
        names.append(name)

print(names)
nameToIdMap = common.mapNamesToIds(names)

s = f"""\
list = {{
    "forbidden": {{
        {buildSection(lflist["banned"], nameToIdMap)}
    }},

    "limited": {{
        {buildSection(lflist["limited"], nameToIdMap)}
    }},

    "semilimited": {{
        {buildSection(lflist["semilimited"], nameToIdMap)}
    }}
}}
"""

print(s)
with open("lflist.py", "w") as f:
    f.write(s)
