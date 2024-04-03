#!/usr/bin/python3
"""
Write a Fabric script that generates a .tgz archive
from the contents of the web_static folder of your
AirBnB Clone repo, using the function do_pack.
"""

from fabric.api import *
from time import strftime


def do_pack():
    """return the archive path if the archive has been correctly generated."""
    a = 'web_static_' + strftime("%Y%m%d%H%M%S") + '.tgz'
    local('mkdir -p versions')
    file = local("tar -czvf versions/{} web_static/".format(a))
    if file is not None:
        return "versions/{}".format(a)
    else:
        return None
