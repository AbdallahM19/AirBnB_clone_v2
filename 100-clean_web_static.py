#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives
"""
import os
from fabric.api import *

env.hosts = ['54.226.45.35', '100.25.46.237']


def do_clean(number=0):
    """Deletes out-of-date archives"""
    number = 1 if int(number) == 0 else int(number)

    # Clean local archives
    local_archives = sorted(os.listdir("versions"))
    [local("rm -f ./versions/{}".format(i)) for i in local_archives[:-number]]

    # Clean remote archives
    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [i for i in archives if "web_static_" in i]
        [run("rm -rf ./{}".format(i)) for i in archives[:-number]]
