#!/usr/bin/python3
"""
    This module deploys our web_static from the archived files
"""
from fabric.api import *
import datetime
import os


def do_pack():
    """Archives our files"""
    time = datetime.datetime.now()
    date = (str(time.year) + str(time.month) + str(time.day) + str(time.hour) +
            str(time.minute) + str(time.second))
    try:
        local("mkdir -p versions")
        local("tar -cvzf versions/web_static_{}.tgz ./web_static".format(date))
        return "./versions/web_static_{}.tgz".format(date)
    except Exception:
        return None


env.hosts = ['35.196.247.36', '35.170.81.242']


def do_deploy(archive_path):
    """Deploys out archived files to remote server and unpacks them"""
    if os.path.exists(archive_path) is False:
        return False
    try:
        upload = put(archive_path, "/tmp/")
        name = archive_path[9:-4]
        rmt_path = "/data/web_static/releases/" + name
        run("mkdir {}".format(rmt_path))
        run("tar -xvzf /tmp/{}.tgz --directory {}/".format(name, rmt_path))
        run("rm /tmp/{}.tgz".format(name))
        run("rm /data/web_static/current")
        run("ln -nsf /data/web_static/releases/{} /data/web_static/current"
            .format(name))
        run("mv {}/web_static/* {}".format(rmt_path, rmt_path))
        run("rm -d {}/web_static/".format(rmt_path))
        return True
    except Exception:
        return False
