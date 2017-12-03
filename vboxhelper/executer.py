import subprocess
import os

class executer:
    def run(command):
        #print(command)
        return subprocess.call(command, shell=True)

    def runwithoutput(command):
        ret = subprocess.call(command, stdout=subprocess.PIPE, shell=True)
        ret.output = ret.stdout.decode('utf-8')
        return ret
