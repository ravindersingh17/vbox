import subprocess
import os

class executer:
    def run(command):
        ret = subprocess.run(command, shell=True)
        return ret.returncode

    def runwithoutput(command):
        ret = subprocess.run(command.split(), stdout=subprocess.PIPE)
        returncode = ret.returncode
        output = ret.stdout.decode('utf-8')
        return { 'returncode': returncode, 'output': output }
