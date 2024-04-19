#!/usr/bin/python3
"""
Write a Fabric script (based on the file 2-do_deploy_web_static.py)
that creates and distributes an archive to your web servers,
using the function deploy:
"""

from fabric.api import *
from os.path import exists, basename
from datetime import datetime


env.hosts = ['52.91.149.30', '18.209.223.47']


def do_deploy(archive_path):
    """Distributes an archive to your web servers"""
    if not exists(archive_path):
        return False
    try:
        archive_name = basename(archive_path)
        archive_folder = '/data/web_static/releases/{}'.format(
            archive_name.split('.')[0])
        put(archive_path, '/tmp/')
        run('sudo mkdir -p {}'.format(archive_folder))
        run('sudo tar -xzf /tmp/{} -C {}'.format(
            archive_name, archive_folder
        ))
        run('sudo rm /tmp/{}'.format(archive_name))
        run('sudo mv {}/web_static/* {}'.format(
            archive_folder, archive_folder
        ))
        run('sudo rm -rf {}/web_static'.format(archive_folder))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s {} /data/web_static/current'.format(
            archive_folder
        ))
        return True
    except Exception:
        return False
