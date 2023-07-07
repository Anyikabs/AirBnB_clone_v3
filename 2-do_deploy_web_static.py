#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import env, put, run
from os.path import exists

env.hosts = ['54.87.210.50', '54.82.137.30']

def do_deploy(archive_path):
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")
        # Get the file name without extension
        file_name = archive_path.split("/")[-1]
        name = file_name.split(".")[0]
        # Uncompress the archive to the folder on the web server
        run("mkdir -p /data/web_static/releases/{}/".format(name))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file_name, name))
        # Delete the archive from the web server
        run("rm /tmp/{}".format(file_name))
        run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(name, name))
        run("rm -rf /data/web_static/releases/{}/web_static".format(name))
        # Delete the symbolic link from the web server
        run("rm -rf /data/web_static/current")
        # Create a new the symbolic link on the web server
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name))
        return True
    except:
        return False
