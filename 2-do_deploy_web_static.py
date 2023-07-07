#!/usr/bin/python3
"""
This script contains the function do_deploy that distributes an archive to our web servers
"""

from fabric.api import put, run, env
import os

env.user = "ubuntu"
env.hosts = ["54.87.210.50", "54.82.137.30"]


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers
    Args:
        archive_path (str): Path to the archive file
    Returns:
        bool: True if successful, False otherwise
    """

    if not os.path.exists(archive_path):
        return False

    archive = os.path.basename(archive_path)
    archive_wout_exten = os.path.splitext(archive)[0]

    if put(archive_path, "/tmp/{}".format(archive)).failed:
        return False

    if run("mkdir -p /data/web_static/releases/{}/".format(archive_wout_exten)).failed:
        return False

    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(archive, archive_wout_exten)).failed:
        return False

    if run("rm /tmp/{}".format(archive)).failed:
        return False

    if run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(archive_wout_exten, archive_wout_exten)).failed:
        return False

    if run("rm -rf /data/web_static/releases/{}/web_static/".format(archive_wout_exten)).failed:
        return False

    if run("rm -rf /data/web_static/current").failed:
        return False

    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(archive_wout_exten)).failed:
        return False

    print("New version deployed!")
    return True
