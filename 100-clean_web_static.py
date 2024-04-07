#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives
"""
import os
from fabric.api import *

env.hosts = ['54.226.45.35', '100.25.46.237']


def do_clean(number=0):
    """Deletes out-of-date archives"""
    number = int(number)
    if number == 0 or number == 1:
        number_to_keep = 1
    else:
        number_to_keep = number

    with lcd("versions"):
        local_archives = sorted(os.listdir("."))
        archives_to_remove = local_archives[:-number_to_keep]
        for archive in archives_to_remove:
            local("rm -f {}".format(archive))

    with cd("/data/web_static/releases"):
        remote_archives = run("ls -tr").split()
        remote_archives = [archive for archive in remote_archives if "web_static_" in archive]
        archives_to_remove = remote_archives[:-number_to_keep]
        for archive in archives_to_remove:
            run("rm -rf {}".format(archive))
