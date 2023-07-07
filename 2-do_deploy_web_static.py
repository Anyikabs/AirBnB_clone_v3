#!/usr/bin/python3
"""This script contains the function do_deploy
that distributes an archive to our web servers
"""

from fabric.api import put, run, env
import os


env.username = "ubuntu"
env.hosts = ["100.26.235.45", "100.25.222.11"]


def do_deploy(archive_path):
    """This function distributes an archive
    to my webservers"""

    if not os.path.exists(archive_path):
        return False

    if put("{}".format(archive_path), "/tmp/").failed:
        return False

    archive = archive_path.split("/")
    archive_w_exten = archive[1]
    archive_wout_exten = archive[1][:-4]

    if run(f"mkdir -p /data/web_static/releases/{archive_wout_exten}/").failed:
        return False

    if run(f"""tar -xzf /tmp/{archive_w_exten} -C /data/web_static/releases/{archive_wout_exten}/""").failed:
        return False

    if run(f"rm /tmp/{archive_w_exten}").failed:
        return False

    if run(f"""mv /data/web_static/releases/{archive_wout_exten}/web_static/* /data/web_static/releases/{archive_wout_exten}/""").failed:
        return False

    if run(f"rm -rf /data/web_static/releases/{archive_wout_exten}/web_static/").failed:
        return False

    if run(f"rm -rf /data/web_static/current").failed:
        return False

    if run(f"ln -s /data/web_static/releases/{archive_wout_exten}/ /data/web_static/current").failed:
        return False

    print("New version deployed!")
    return True
