#!/usr/bin/python3
"""
Write a Fabric script (based on the file 2-do_deploy_web_static.py)
that creates and distributes an archive to your web servers,
using the function deploy:
"""

from fabric.api import *
from os.path import exists, basename
from datetime import datetime


env.hosts = ['52.87.212.96', '100.25.46.237']


def do_pack():
    """
    Packs all files in web_static to versions folder with name
    web_static_<year><month><day><hour><minute><second>.tgz
    """
    try:
        time = datetime.now().strftime("%Y%m%d%H%M%S")
        if not exists('versions'):
            local("mkdir -p versions")
        file_name = "versions/web_static_{}.tgz".format(time)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except Exception as e:
        return None


def do_deploy(archive_path):
    """
    Deploys the archive to the web server
    """
    if not exists(archive_path):
        return False
    try:
        archive_file = archive_path.split('/')[-1]
        archive_name = archive_file.split('.')[0]
        archive_folder = '/data/web_static/releases/{}'.format(
            archive_name
        )
        put(archive_path, '/tmp/{}'.format(archive_file))
        run("rm -rf {}/".format(archive_folder))
        run('mkdir -p {}/'.format(archive_folder))
        run('tar -xzf /tmp/{} -C {}/'.format(
            archive_file, archive_folder
        ))
        run('rm /tmp/{}'.format(archive_file))
        run('mv {}/web_static/* {}/'.format(
            archive_folder, archive_folder
        ))
        run('rm -rf {}/web_static'.format(archive_folder))
        run('rm -rf /data/web_static/current')
        run('ln -s {}/ /data/web_static/current'.format(
            archive_folder
        ))
        return True
    except Exception as e:
        return False


def deploy():
    """Full deployment process"""
    a_path = do_pack()
    if not a_path:
        return False
    return do_deploy(a_path)
