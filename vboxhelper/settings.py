import json, os

class settings:

    def __init__():
        homeDir = os.path.expanduser("~")
        self.dataFile = os.path.join(homeDir, ".vbox", "data.json")
        self.data = json.loads(open(dataFile).read())

    def getAll():
        return self.data

    def writeToDisk():
        fhandle = open(self.dataFile, 'w')
        fhandle.write(json.dumps(data))
