#!/bin/env python3

import sys, os, re, argparse, platform

from vboxhelper.executer import executer
from vboxhelper.settings import settings
from vboxhelper.dnsmanager import dnsmanager
from vboxhelper.VBoxException import VBoxException

class vbox:
    """
    Module that provides most of the functionality of VirtualBox manager
    """

    settings = VBoxSettings()

    def _getplatform():
        ostype = platform.system()
        if ostype == "Windows": return "WINDOWS"
        elif ostype == "Linux": return "LINUX"
        elif ostype[:6] == "CYGWIN": return "CYGWIN"
        else: return False

    def _addstoragectl(vmname, ctlname, ctltype):
        vbox._shellrunner("VBoxManage storagectl \"{0}\" --name {1} --add {2}", (vmname, ctlname, ctltype))

    def _getwinpath(path):
        ret = vbox._shellrunner("cygpath -w \"{0}\"", (path, ), True)
        return ret.output.strip()

    def _getcygpath(path):
        ret = vbox._shellrunner("cygpath \"{0}\"", (path.replace("\\", "\\\\"), ), True)
        return ret.output.strip()

    def _modifymem(vmname, mem):
        vbox._shellrunner("VBoxManage modifyvm \"{0}\" --memory {1}", (vmname, mem))

    def _storageattach(vmname, mediumpath, storagectl, disktype, port = 0, device = 0):
        vbox._shellrunner("VBoxManage storageattach \"{0}\" --storagectl {1} --port {2} --device {3} --type {4} --medium \"{5}\"", (vmname, storagectl, port, device, disktype, mediumpath))

    def _modifynic(vmname, nicnum, adaptertype):
        vbox._shellrunner("VBoxManage modifyvm \"{0}\" --nic{1} {2}", (vmname, nicnum, adaptertype))

    def _setextradata(vmname, datakey, datavalue):
        vbox._shellrunner("VBoxManage setextradata \"{0}\" \"{1}\" \"{2}\"", (vmname, datakey, datavalue))

    def _getextradata(vmname, datakey):
        ret = vbox._shellrunner("VBoxManage getextradata \"{0}\" \"{1}\"", (vmname, datakey), True)
        if ret.output.strip() == "No value set!": return None
        else:
            match = re.match("Value:\s*(.*)", ret.output.strip())
            return match.group(1)

    def _getvmdata(onlyrunning = False):
        listof = "vms"
        if onlyrunning: listof = "runningvms"
        ret = vbox._shellrunner("VBoxManage list {0}", (listof, ), True)
        matches = re.findall('"(.*?)"\s*\{(.*?)\}', ret.output, re.M)
        vmdata = []
        for x in matches: vmdata.append({"name": x[0], "uuid": x[1], "netid": vbox._getextradata(x[0], "ID"), "hostname": vbox._getextradata(x[0],"hostname")})
        return vmdata

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

    def func_debug(p):
        a = vbox._getextradata("Ubuntu GUI VM", "foo bar")
        print("\"{0}\"".format(a))


    def help_main():
        """
        The help function for help without parameters

        Returns: String with help information
        """
        return("""Usage: vbox [action] [vmname] [parameters]
        Action is:
            help [action]
            list
            listrunning
            create --name <name> --hostname <hostname> --id <ID> --ostype <ostype> --mem <memory> --disk <disksize> [--iso <isopath>]
            start <vmname>
            startgui <vmname>
            reset <vmname>
            poweroff <vmname>
            powerbutton <vmname>
            addiso <isopath> [--ctl <storage controller>] [--port <portnum] [--device <devicenum>]
        Use vbox help <action> to get help on action
        """)

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
        except IndexError:
            print(vbox.help_main())
        else:
            func()

    def func_create(p):
        """
        Function to create VM

        Args:
            p: Parameters Object
        """
        p.add_argument("--name", required=True)
        p.add_argument("--host", required=True)
        p.add_argument("--ostype", required=True)
        p.add_argument("--id", required=True)
        p.add_argument("--mem", required=True)
        p.add_argument("--disk", required=True, type=float)
        p.add_argument("--iso")
        p.add_argument("--vmpath")

        if p: opts = p.parse_args()

        vmdata = vbox._getvmdata()

        if opts.name in [x[0] for x in vmlist]:
            print("VM with the same name already exists")
            return False

        if vbox._getplatform() == "CYGWIN":
            if opts.vmpath :
                vmpath = vbox._getwinpath(opts.vmpath)
            else:
                vmpath = vbox._getwinpath(vbox.settings.disk_path)
        else:
            if opts.vmpath: vmpath = opts.vmpath
            else:
                vmpath = vbox.settings.disk_path

        if not vmpath:
            raise VBoxException("Path not specified and does not exist in settings")


        vbox._shellrunner("VBoxManage createvm --name \"{0}\" --ostype {1} --register", (opts.name, opts.ostype))

        vbox._addstoragectl(opts.name, "IDE", "ide")
        vbox._addstoragectl(opts.name, "SATA", "sata")

        vbox._modifymem(opts.name, opts.mem)

        if vbox._getplatform() == "CYGWIN":
            storagepath = vbox._getcygpath(vmpath)
            vdifilepath = vmpath.strip("\\") + "\\{0}\\{0}.vdi".format(opts.name)
        else:
            storagepath = vmpath
            vdifilepath = os.path.join(storagepath, opts.name, "{0}.vdi".format(opts.name))

        if not os.path.exists(os.path.join(storagepath, opts.name)): os.mkdir(os.path.join(storagepath, opts.name))

        vbox._shellrunner("VBoxManage createmedium disk --filename \"{0}\" --size {1} --format VDI --variant Standard", (vdifilepath, int(opts.disk * 1024)))

        vbox._storageattach(opts.name, vdifilepath, "SATA", "hdd")

        vbox._modifynic(opts.name, 1, 'nat')
        vbox._modifynic(opts.name, 2, 'hostonly')
        vbox._modifynic(opts.name, 3, 'intnet')

        if opts.iso:
            isopath = opts.iso
            if vbox._getplatform() == "CYGWIN": isopath = vbox._getwinpath(opts.iso)
            vbox._storageattach(opts.name, isopath, "IDE", "dvddrive")

        if opts.id in [ x["netid"] for x in vmdata ]: print("ID is already taken, run vbox updatesetings <vmname> to correct setting")
        if opts.hostname in [ x["hostname"] for x in vmdata ]: print("Hostname is already taken, run vbox updatesettings <vmname to correct setting")

        dns = dnsmanager(vbox.settings.bind_path)
        dns.update(opts.name, opts.id, opts.host)

    def help_create():
        print("Usage: vbox create --name <name> --host <hostname> --id <id> --ostype <ostype> --mem <mem> --disk <disk> [--iso <isopath>]")

    def func_list(p, onlyrunning=False, returnvms=False):
        """
        Lists all VMs or running VMs

        Args:
            p: Parameters object
            onlyrunning: Display all VMs or running VMs

        Returns:
            Bool True if command succeeds, False if parameter AttributeError
        """
        if onlyrunning: suffix = "runningvms"
        else: suffix = "vms"

        return True

    def help_list():
        """
        Help function for vbox list
        """
        print("Usage: vbox list")

    def func_listrunning(p, returnvmms=False):
        """
        List running VMs

        Args:
            p: Parameters object

        Returns:
            output of func_list
        """
        return vbox.func_list(p, True, returnvms)

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

    def func_setextradata(p):
        """
        Set VM extradata

        Args:
            p: Parameters object
        Returns:
            True if command succeeds, false on parameter error
        """
        p.add_argument("--key", required=True)
        p.add_argument("--value", required=True)
        opts = p.parse_args()
        if len(opts.cmd) != 2:
            help_setextradata()
            return False
        vbox._setextradata(opts.cmd[1], opts.key, opts.value)
        return True

    def help_setextradata():
        """
        Help for vbox setextradata
        """
        print("Usage: vbox setextradata <vmname> --key <key> --value <value>")


def main():
    """
    Entry point for vbox manager
    """
    p = argparse.ArgumentParser(description="VBox argument parser", usage=vbox.help_main())
    p.add_argument('cmd', nargs="+", help="action")
    if len(sys.argv) == 0:
        print("Please use an action")
        print(vbox.help_main())
        sys.exit(1)
    try:
        func = getattr(vbox, "func_" + sys.argv[1])
    except AttributeError:
        print("Invalid command")
        print(vbox.help_main())
        sys.exit(-1)
    else: func(p)

