#!/bin/env python3

from distutils.core import setup
from distutils.command.install import install
import os, json

class vboxcustom(install):

    def run(self):
        settings_file = os.path.expanduser("~/.vbox")
        disk_path = input("Enter destination path for disk files (Default: {0}):".format(os.path.expanduser("~/vbox VMs")))
        host_net = input("Enter host only network. Default 192.168.56.x:")
        internal_net = input("Enter internal network. Default 192.168.100.x:")

        if disk_path is "": disk_path = os.path.expanduser("~/vbox VMs")
        if host_net is "": host_net = "192.168.56.x"
        if internal_net is "": internal_net = "192.168.100.x"

        settings = {"disk_path": disk_path, "host_net": host_net, "internal_net": internal_net }

        f = open(settings_file, 'w')
        f.write(json.dumps(settings))

        super(vboxcustom, self).run()

setup(
        name="vbox",
        version="1.0",
        description="VirtualBox manager",
        author="Ravinder Singh",
        author_email="ravinder.ssgh@gmail.com",
        url="https://github.com/ravindersingh17/vbox",
        packages=["vboxhelper"],
        scripts=["scripts/vbox"],
        cmdclass={
            "install": vboxcustom,
            }
        )

