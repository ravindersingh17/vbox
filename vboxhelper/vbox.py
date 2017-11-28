#!/bin/env python3

import sys, os
import argparse

from vboxhelper.executer import executer
from vboxhelper.VBoxException import VBoxException

class vbox:

    def _addiso(vmname, path):
        if path == "additions":
            pathfinal = path
        else:
            runwithoutput("foo")

        #executer.run("VBoxManage storageattach \"{0}\" --storagectl IDE --port 0 --device 0 --type dvddrive

    def _iscygwin():
        sysname = executer.runwithoutput("uname -s")["output"][0]
        if sysname[:6] == "CYGWIN":
            return True
        return False

    def _getActualPath():
        pass

    def _shellrunner(cmd, params, returnoutput=False):
        """
        Execute a virtualbox command in shell

        Args:
            cmd: The command to execute with placeholders
            params: The parameters to cmd
            returnoutput: True to return the output. False to pass it to stdout

        Returns:
            Dictionary with keys returncode and output.

        Raises:
            VBoxException: If command fails
        """
        if returnoutput:
            func = getattr(executer, "runwithoutput")
        else:
            func = getattr(executer, "run")
        ret = func(cmd.format(*params))
        if ret.returncode != 0: raise VBoxException("VBoxManage returned error status:{0}".format(ret.returncode))
        return ret



    def func_help(p):
        """
        Give help for vbox subcommands

        Args:
            p: Parameters object
        
        Returns:
            Boolean true on success, false otherwise
        """
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

    def func_list(p, onlyrunning=False):
        """
        Lists all VMs or running VMs

        Args:
            p: Parameters object
            onlyrunning: Display all VMs or running VMs

        Returns:
            Bool True if command succeeds, False if parameter AttributeError
        """
        opts = p.parse_args()
        if onlyrunning: suffix = "runningvms"
        else: suffix = "vms"

        ret = vbox._shellrunner("VBoxManage list {0}", (suffix, ), True)
        print(ret.output)
        return True

    def help_list():
        """
        Help function for vbox list
        """
        print("Usage: vbox list")

    def func_listrunning(p):
        """
        List running VMs

        Args:
            p: Parameters object
        
        Returns:
            output of func_list
        """
        return vbox.func_list(p, True)

    def help_listrunning():
        """
        Help on vbox listrunning
        """
        print("Usage: vbox listrunning")


    def func_start(p, gui=False):
        """
        Start a VM

        Args:
            p: Parameters  object
            gui: Whether to run VirtualBox GUI or headless

        Returns:
            Bool True if command succeeds, false on parameter error
        """

        opts = p.parse_args()
        if len(opts.cmd) != 2:
            help_start()
            return False
        suffix = "--type headless"
        if gui: suffix = ""
        vbox._shellrunner("VBoxManage startvm \"{0}\" {1}", (opts.cmd[1], suffix))
        return True

    def help_start():
        """
        Print help for vbox start
        """
        print("Usage: vbox start <vmname>")

    def func_startgui(p):
        """
        Start a VM with GUI

        Args:
            p: Parameters object

        Returns:
            Output of func_start
        """
        return vbox.func_start(p, True)

    def help_startgui():
        """
        Print help for vboxstartgui
        """
        print("Usage: vbox startgui <vmname>")

    def func_save(p):
        """
        Save a VM state

        Args:
            p: Parameters object

        Returns:
            True if command succeeds, false on parameter error
        """
        opts = p.parse_args()
        if len(opts.cmd) != 2:
            help_save()
            return False
        vbox._shellrunner("VBoxManage controlvm \"{0}\" savestate", (opts.cmd[1], ))
        return True

    def help_save():
        """
        Help on vbox save
        """
        print("Usage: vbox save <vmname>")

    def func_reset(p):
        """
        Restart a VM

        Args:
            p: Parameters object

        Returns:
            True if command succeeds, false on parameter error
        """
        opts = p.parse_args()
        if len(opts.cmd) != 2:
            help_reset()
            return False
        vbox._shellrunner("VBoxManage controlvm \"{0}\" reset", (opts.cmd[1], ))
        return True

    def help_reset(p):
        """
        Help on vbox reset
        """
        print("Usage vbox reset <vmname>")

    def func_poweroff(p):
        """
        Power off VM

        Args:
            p: Parameters object

        Returns:
            True if commmand succeeds, false on parameter error
        """
        opts = p.parse_args()
        if len(opts.cmd) != 2:
            help_poweroff()
            return False
        vbox._shellrunner("VBoxManage controlvm \"{0}\" poweroff", (opts.cmd[1], ))
        return True

    def help_poweroff():
        """
        Help on vbox poweroff
        """
        print("Usage: vbox poweroff <vmname>")

    def func_powerbutton(p):
        """
        Send ACPI poweroff to VM

        Args:
            p: Parameters object

        Returns:
            True if command succeeds, false on parameter error
        """
        opts = p.parse_args()
        if len(opts.cmd) != 2:
            help_powerbutton()
            return False
        vbox._shellrunner("VBoxManage controlvm \"{0}\" acpipowerbutton", (opts.cmd[1], ))
        return True

    def help_powerbutton():
        """
        Help on vbox powerbutton
        """
        print("Usage: vbox powerbutton <vmname>")

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
    if len(sys.argv) == 0:
        print("Please use an action")
        print(help_main)
        sys.exit(1)
    try:
        func = getattr(vbox, "func_" + sys.argv[1])
    except AttributeError:
        print("Invalid command")
        print(help_main)
        sys.exit(-1)
    else: func(p)

