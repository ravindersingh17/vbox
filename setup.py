from setuptools import setup
from setuptools.command.install import install
from setuptools.command.develop import develop
import os, json, sys

class vboxinstallcommon:
    user_options = [
            ("disk-path=", None, "Location where vbox disk files will be stored."),
            ("host-net=", None, "Network for host only network. Default 192.168.56.x"),
            ("int-net=", None, "Network for internal network. Default 192.168.100.x"),
                  ]

    default_disk_path = os.path.join(os.path.expanduser("~"), "vbox VMs")
    default_host_net = "192.168.56.x"
    default_int_net = "192.168.100.x"

    def run(settings):
        vboxdir = os.path.join(os.path.expanduser("~"), ".vbox")
        if not os.path.exists(vboxdir):
            os.makedirs(vboxdir)
        settings_file = os.path.join(os.path.expanduser("~"), ".vbox", "data.json")

        handle = open(settings_file, "w")
        handle.write(json.dumps(settings))
        handle.close()

class vboxcustom(install):
    user_options = install.user_options + vboxinstallcommon.user_options

    def initialize_options(self):
        self.disk_path = None
        self.host_net = None
        self.int_net = None
        super(vboxcustom, self).initialize_options()

    def finalize_options(self):
        if self.disk_path is None:
            self.disk_path = vboxinstallcommon.default_disk_path
        if self.host_net is None:
            self.host_net = vboxinstallcommon.default_host_net
        if self.int_net is None:
            self.int_net = "192.168.100.x"
        super(vboxcustom, self).finalize_options()

    def run(self):
        settings = {"disk_path": self.disk_path, "host_net": self.host_net, "int_net": self.int_net }
        vboxinstallcommon.run(settings)

        super(vboxcustom, self).run()

class vboxcustomdevelop(develop):
    user_options = develop.user_options + vboxinstallcommon.user_options

    def initialize_options(self):
        self.disk_path = None
        self.host_net = None
        self.int_net = None
        super(vboxcustomdevelop, self).initialize_options()

    def finalize_options(self):
        if self.disk_path is None:
            self.disk_path = vboxinstallcommon.default_disk_path
        if self.host_net is None:
            self.host_net = vboxinstallcommon.default_host_net
        if self.int_net is None:
            self.int_net = vboxinstallcommon.default_int_net
        super(vboxcustomdevelop, self).finalize_options()

    def run(self):
        settings = {"disk_path": self.disk_path, "host_net": self.host_net, "int_net": self.int_net }
        vboxinstallcommon.run(settings)
        super(vboxcustomdevelop, self).run()

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
            "develop": vboxcustomdevelop,
            }
        )

