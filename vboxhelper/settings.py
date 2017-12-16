import json, os

class settings:

    def __init__(self):
        homeDir = os.path.expanduser("~")
        self.dataFile = os.path.join(homeDir, ".vbox", "data.json")
        self.data = json.loads(open(dataFile).read())

    def getAll(self):
        return self.data

    def writeToDisk(self):
        fhandle = open(self.dataFile, 'w')
        fhandle.write(json.dumps(data))
