import requests
import time
import json
import os

def download(url, timestampFile, dataFile):
    print("Downloading " + url + " ...")
    r = requests.get(url)

    if not r.ok:
        print("Request failed")
        print(r.text)
        exit(1)

    print("Finished downloading!")

    _json = r.json()
    timestamp = int(time.time())

    with open(dataFile, "w") as f:
        json.dump(_json, f, indent=4, ensure_ascii=False)

    with open(timestampFile, "w") as f:
        f.write(str(timestamp))

    return _json


def load(url, name):
    cacheDir = "cache/"
    timestampFile = cacheDir + name + ".timestamp"
    dataFile = cacheDir + name + ".json"

    exists = os.path.isfile

    if not exists(timestampFile) or not exists(dataFile):
        return download(url, timestampFile, dataFile)

    now = int(time.time())
    lastDownloadTime = -1

    with open(timestampFile) as f:
        lastDownloadTime = int(f.read())
    
    _24HoursAsSeconds = 60 * 60 * 24

    if now - lastDownloadTime > _24HoursAsSeconds:
        return download(url, timestampFile, dataFile)

    with open(dataFile) as f:
        return json.load(f)
