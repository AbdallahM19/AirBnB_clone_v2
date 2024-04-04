#!/usr/bin/python3
"""
Write a Fabric script (based on the file 2-do_deploy_web_static.py)
that creates and distributes an archive to your web servers,
using the function deploy:
"""

from fabric.api import *
from os.path import exists, basename
from datetime import datetime


env.hosts = ['54.85.96.172', '54.210.130.17']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_pack():
    """
    Packs all files in web_static to versions folder with name
    web_static_<year><month><day><hour><minute><second>.tgz
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        if not exists('versions'):
            local("mkdir -p versions")
        filename = "versions/web_static_{}.tgz".format(timestamp)
        local("tar -cvzf {} web_static".format(filename))
        return filename
    except Exception:
        return None


def do_deploy(archive_path):
    """
    Deploys the archive to the web server
    """
    if not exists(archive_path):
        return False
    try:
        archive_name = archive_path.split('/')[1]
        archive_folder = '/data/web_static/releases/{}'.format(
            archive_name.split('.')[0]
        )
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


def deploy():
    """Full deployment process"""
    a_path = do_pack()
    if not a_path:
        return False
    return do_deploy(a_path)
