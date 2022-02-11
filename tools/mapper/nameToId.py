import common

with open("namesInput.txt", "r") as f:
    names = f.readlines()
    names = [line.strip().lower() for line in names]

ids = []
successful = True
nameToIdMap = common.mapNamesToIds(names)
for name in names:
    ids.append(nameToIdMap[name])

with open("out.txt", "w") as f:
    ids = [str(id) for id in ids]
    s = "\n".join(ids)
    f.write(s)
