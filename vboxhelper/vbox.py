#!/bin/env python3

import sys, os
import argparse

from vboxhelper import executer

class vbox:

    def _addiso(vmname, path):
        if path == "additions":
            pathfinal = path
        else:
            runwithoutput("foo")

        #executer.run("VBoxManage storageattach \"{0}\" --storagectl IDE --port 0 --device 0 --type dvddrive

    def _isCygwin():
        sysname = executer.runwithoutput("uname -s")["output"][0]
        if sysname[:6] == "CYGWIN":
            return True
        return False

    def _getActualPath():
        pass


    def func_help(p):
        opts = p.parse_args()
        try:
            func = getattr(vbox, "help_" + opts.cmd[1])
        except AttributeError:
            print("Invalid action")
        else:
            func()



    def func_create(p):
        p.add_argument("--name", required=True)
        p.add_argument("--host", required=True)
        p.add_argument("--ostype", required=True)
        p.add_argument("--mem", required=True)
        p.add_argument("--disk", required=True, type=float)
        p.add_argument("--iso")

        opts = p.parse_args()
        if executer.run("VBoxManage createvm --name \"{0}\" --ostype \"{1}\" --register".format(opts.name, opts.ostype)) != 0:
            print("Unable to create VM")
            return False

        if executer.run("VBoxManage storagectl \"{0}\" --name IDE --add ide".format(opts.name)) != 0:
            print("Unable to add IDE storage controller")
            return False

        if executer.run("VBoxManage storagectl \"{0}\" --name SATA --add sata".format(opts.name)) != 0:
            print("Unable to add SATA storage controller")
            return False

        os.mkdir(basedir + opts.name)



    def help_create():
        print("Usage: vbox create --name <name> --host <hostname> --id <id> --ostype <ostype> --mem <mem> --disk <disk> [--iso <isopath>]")

    def func_list(p):
        opts = p.parse_args()
        print(opts)

    def func_start(p):
        opts = p.parse_args()
        print(opts)

    def func_addiso(p):
        opts = p.parse_args()
        if len(opts.cmd) != 3:
            print("Invalid parameters")
            vbox.help_addiso()

    def help_addiso():
        print("Usage: vbox addiso <guest|isopath>")

def main():
    help_main = """Usage: vbox [action] [vmname] [parameters]
    Action is:
        list
        listrunning
        create
        addiso
    Use vbox help <action> to get help on action
    """
    p = argparse.ArgumentParser(description="VBox argument parser", usage=help_main)
    p.add_argument('cmd', nargs="+", help="action")
    try:
        func = getattr(vbox, "func_" + sys.argv[1])
    except AttributeError:
        print("Invalid command")
        print(help_main)
        sys.exit(-1)
        sys.exit()
    func(p)

