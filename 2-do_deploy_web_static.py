#!/usr/bin/env bash
# This script contains the function do_deploy
# that distributes an archive to our web servers

from fabric import Connection
import os


env = {
    'username': 'ubuntu',
    'hosts': ['54.87.210.50', '54.82.137.30']
}


def do_deploy(archive_path):
    """This function distributes an archive
    to the web servers"""

    if not os.path.exists(archive_path):
        print(f"Archive file '{archive_path}' not found.")
        return False

    with Connection(env['hosts'][0], user=env['username']) as conn:
        # Upload the archive to the remote server
        result = conn.put(archive_path, '/tmp/')
        if result.failed:
            print("Failed to upload the archive.")
            return False

        # Extract the archive to the desired location
        archive_name = os.path.basename(archive_path)
        archive_folder = os.path.splitext(archive_name)[0]
        target_folder = f"/data/web_static/releases/{archive_folder}"
        result = conn.run(f"mkdir -p {target_folder}")
        if result.failed:
            print("Failed to create the target folder.")
            return False

        result = conn.run(f"tar -xzf /tmp/{archive_name} -C {target_folder}")
        if result.failed:
            print("Failed to extract the archive.")
            return False

        # Move the contents of the extracted folder
        result = conn.run(f"mv {target_folder}/web_static/* {target_folder}")
        if result.failed:
            print("Failed to move the contents of the extracted folder.")
            return False

        # Remove unnecessary folder and files
        result = conn.run(f"rm -rf {target_folder}/web_static")
        if result.failed:
            print("Failed to remove the unnecessary folder.")
            return False

        result = conn.run("rm /tmp/{}".format(archive_name))
        if result.failed:
            print("Failed to remove the archive file from /tmp/ directory.")
            return False

        # Update the symbolic link
        current_link = "/data/web_static/current"
        result = conn.run(f"rm -rf {current_link}")
        if result.failed:
            print("Failed to remove the current symlink.")
            return False

        result = conn.run(f"ln -s {target_folder} {current_link}")
        if result.failed:
            print("Failed to create the new symlink.")
            return False

    print("New version deployed!")
    return True
