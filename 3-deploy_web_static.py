#!/usr/bin/python3
"""This script does a full deploy on my webservers"""


from fabric.api import local, run, put, env
do_pack = __import__("1-pack_web_static").do_pack
do_deploy = __import__("2-do_deploy_web_static").do_deploy


def deploy():
    """This function does full deployment of files to webservers"""

    archive_path = do_pack()
    if archive_path is None:
        return False
    result = do_deploy(archive_path)

    return result
