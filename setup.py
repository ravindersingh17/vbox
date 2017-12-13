from setuptools import setup
from setuptools.command.install import install
import os, json, sys

class vboxcustom(install):
    user_options = install.user_options + [
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
        settings_file = os.path.expanduser("~/.vbox")

        settings = {"disk_path": self.disk_path, "host_net": self.host_net, "int_net": self.int_net }

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
        python_requires=">=3",
        install_requires=["dnspython"],
        packages=["vboxhelper"],
        scripts=["scripts/vbox"],
        cmdclass={
            "install": vboxcustom,
            }
        )

