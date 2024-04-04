#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives
"""

from fabric.api import *
import os
from datetime import datetime

env.hosts = ['54.85.96.172', '54.210.130.17']


def do_clean(number=0):
    """
    Deletes out-of-date archives
    """
    number = 1 if int(number) == 0 else int(number)

    archive = sorted(os.listdir("versions"))
    [archive.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archive]

    with cd("/data/web_static/releases"):
        archive = run("ls -tr").split()
        archive = [a for a in archive if "web_static_" in a]
        [archive.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archive]
