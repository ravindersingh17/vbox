from setuptools import setup
from setuptools import Command
import os, json, sys

class vboxcustom(Command):
    user_options = [
            ("disk-path=", None, "Location where vbox disk files will be stored."),
            ("host-net=", None, "Network for host only network. Default 192.168.56.x"),
            ("int-net=", None, "Network for internal network. Default 192.168.100.x"),
                  ]

    def initialize_options(self):
        self.disk_path = None
        self.host_net = None
        self.int_net = None

    def finalize_options(self):
        if self.disk_path is None:
            self.disk_path = os.path.expanduser("~/vbox VMs")
        if self.host_net is None:
            self.host_net = "192.168.56.x"
        if self.int_net is None:
            self.int_net = "192.168.100.x"

    def run(self):
        print(self.disk_path)
        print(self.host_net)
        print(self.int_net)
        sys.exit()
        settings_file = os.path.expanduser("~/.vbox")

        settings = {"disk_path": self.disk_path, "host_net": self.host_net, "internal_net": self.int_net }

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

