#!/usr/bin/env python

from setuptools import setup
import os

# os.system("sh libinstall.sh")

setup(
    name="yousmileiserve",
    version="0.1.0",
    description="A order robot which makes people better",
    entry_points={
        "console_scripts": ["YouSmileIServe = YouSmileIServe.main_service:run_cli",
                            "menu = YouSmileIServe.menu_manager:run_cli"],
                            #"menu-gui = YouSmileIServe.menugui:run_gui"]
        'gui_scripts': ["menu-gui=YouSmileIServe.menugui:run_gui"]
        #"console_scripts": ["menu = YouSmileIServe.menu_manager:run_cli"]
    },
    classifiers=[
        "Natural Language :: English",
        "Programming Language :: Python :: 3.5",
    ],
    author="EE303",
    packages=["YouSmileIServe", "YouSmileIServe.CamUtils", "YouSmileIServe.menu", "YouSmileIServe.menugui"],
    include_package_data=True,
    zip_safe=False,
    package_data={
        '': ['*.txt', '*.ui']
    })
