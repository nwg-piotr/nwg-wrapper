#!/usr/bin/env python3

import os
import subprocess
from shutil import copyfile


def get_config_dir():
    """
    Determine config dir path, create if not found, then create sub-dirs
    :return: config dir path
    """
    xdg_config_home = os.getenv('XDG_CONFIG_HOME')
    config_home = xdg_config_home if xdg_config_home else os.path.join(os.getenv("HOME"), ".config")
    config_dir = os.path.join(config_home, "nwg-wrapper")
    if not os.path.isdir(config_dir):
        print("Creating '{}'".format(config_dir))
        os.mkdir(config_dir)

    return config_dir


def copy_files(src_dir, dst_dir):
    src_files = os.listdir(src_dir)
    for file in src_files:
        if os.path.isfile(os.path.join(src_dir, file)):
            if not os.path.isfile(os.path.join(dst_dir, file)):
                copyfile(os.path.join(src_dir, file), os.path.join(dst_dir, file))
                print("Copying '{}'".format(os.path.join(dst_dir, file)))


def script_output(path):
    try:
        lines = subprocess.check_output(path).decode("unicode_escape").splitlines()
        output = ""
        for line in lines:
            output += line + "\n"
        # remove trailing "\n"
        output = output[:-1]
    except Exception as e:
        output = '<span size="large">Error</span>\\n<i>{} not found</i>'.format(path)
        print(e)
        
    return output
