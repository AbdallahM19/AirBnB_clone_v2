#!/usr/bin/python3
"""Script that generates a .tgz archive from the contents of the web_static."""

from fabric.api import local, env, put, run
from datetime import datetime
import os.path
env.hosts = ['52.91.149.30', '18.209.223.47']


def do_pack():
    """Function to generate a .tgz archive."""
    # Create the folder versions if not exists
    local("mkdir -p versions")
    # Get the current date and time in the format YYYYMMDDHHMMSS
    current_date = datetime.now().strftime("%Y%m%d%H%M%S")
    # Create the name of the file
    # The file name has the format: web_static_YYYYMMDDHHMMSS.tgz
    file = "versions/web_static_{}.tgz".format(current_date)
    try:
        # Compress the files
        local("tar -cvzf {} web_static".format(file))
        # If the file was created
        return file
    except Exception as execption:
        # If the file doesn't be created return None
        return None


def do_deploy(archive_path):
    """Distributes an archive to your web servers."""
    # command to run: fab -f 2-do_deploy_web_static.py -->
    # --> do_deploy:archive_path=versions/web_static_20231005205444.tgz -->
    # -i ~/.ssh/id_rsa -u ubuntu
    # if the path doesn't exist
    if not os.path.exists(archive_path):
        return False
    try:
        # getting the file name from the path
        filename = archive_path.split("/")[-1]
        # getting the file name without the extension .tgz
        no_extension = filename.split(".")[0]
        # uploading the file to /tmp/ directory
        put(archive_path, "/tmp/")
        # creating the directory where the file will be uncompressed
        run("mkdir -p /data/web_static/releases/{}/".format(no_extension))
        # uncompressing the archive to the folder created in the previous step
        # -x flag is used to extract the files from the archive
        # -z flag is used to uncompress the files from .tgz archive
        # -f flag is used to specify the file name of the archive
        # -C flag is used to uncompress the files to the folder specified
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(filename, no_extension))
        # deleting the archive from the web server
        run("rm /tmp/{}".format(filename))
        # moving the files to the folder created in the previous step
        run("mv /data/web_static/releases/{}/web_static/*\
            /data/web_static/releases/{}/".format(no_extension, no_extension))
        # deleting the folder web_static
        run("rm -rf /data/web_static/releases/{}/web_static"
            .format(no_extension))
        # deleting the symbolic link from the web server
        run("rm -rf /data/web_static/current")
        # creating a new symbolic link on the web server
        # linked to the new version of the code deployed on the web server
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(no_extension))
        return True
    except Exception as e:
        return False
