#!/bin/env python3

from distutils.core import setup

setup(
        name="vbox",
        version="1.0",
        description="VirtualBox manager",
        author="Ravinder Singh",
        author_email="ravinder.ssgh@gmail.com",
        url="https://github.com/ravindersingh17/vbox",
        #py_modules=["vbox", "executer"],
        packages=["vboxhelper"],
        scripts=["scripts/vbox"],
        )

