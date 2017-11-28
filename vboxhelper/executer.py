import subprocess
import os

class executer:
    def run(command):
        return subprocess.run(command, shell=True)

    def runwithoutput(command):
        ret = subprocess.run(command, stdout=subprocess.PIPE, shell=True)
        ret.output = ret.stdout.decode('utf-8')
        return ret
