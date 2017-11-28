import subprocess

class executer:
    def run(command):
        ret = subprocess.run(command, shell=True)
        return ret.returncode

    def runwithoutput(command):
        ret = subprocess.run(command.split(), stdout=subprocess.PIPE, stderr=stdout)
        returncode = ret.returncode
        output = str(ret.stdout).split()
        return { 'returncode': returncode, 'output': output }
