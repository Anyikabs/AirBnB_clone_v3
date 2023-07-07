#!/usr/bin/python3
"""This script generates a .tgz archive
from the contents of the web_static directory
"""


from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """This funcion archives and compresses
    all the contents of the web_static folder"""

    today = datetime.today()
    path_to_archive = "versions/web_static_{}{}{}{}{}.tgz".format(
                       today.year, today.month, today.day, today.hour,
                       today.minute, today.second)
    print("Packing web_static to {}".format(path_to_archive))

    if not os.path.exists("versions/"):
        local("mkdir versions/")

    if local("tar -cvzf {} web_static".format(path_to_archive)).succeeded:
        return path_to_archive
    else:
        return None
