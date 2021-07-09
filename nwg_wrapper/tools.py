#!/usr/bin/env python3

import os
import sys
import subprocess
from shutil import copyfile

import gi
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk, Gdk, GdkPixbuf

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


def is_command(cmd):
    cmd = cmd.split()[0]  # strip arguments
    cmd = "command -v {}".format(cmd)
    try:
        is_cmd = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
        if is_cmd:
            return True

    except subprocess.CalledProcessError:
        return False


def list_outputs():
    """
    Get output names and geometry from i3 tree, assign to Gdk.Display monitors.
    :return: {"name": str, "x": int, "y": int, "width": int, "height": int, "monitor": Gkd.Monitor}
    """
    outputs_dict = {}
    sway = os.getenv('SWAYSOCK')
    if sway:
        print("Running on sway")
        try:
            from i3ipc import Connection
        except ModuleNotFoundError:
            print("'python-i3ipc' package required on sway, terminating")
            sys.exit(1)

        i3 = Connection()
        tree = i3.get_tree()
        for item in tree:
            if item.type == "output" and not item.name.startswith("__"):
                outputs_dict[item.name] = {"x": item.rect.x,
                                           "y": item.rect.y,
                                           "width": item.rect.width,
                                           "height": item.rect.height}
    # Try wlr-randr if we're not on sway
    elif os.getenv('WAYLAND_DISPLAY') is not None:
        print("Running on Wayland, but not sway")
        if is_command("wlr-randr"):
            lines = subprocess.check_output("wlr-randr", shell=True).decode("utf-8").strip().splitlines()
            if lines:
                name, w, h, x, y = None, None, None, None, None
                for line in lines:
                    if not line.startswith(" "):
                        name = line.split()[0]
                    elif "current" in line:
                        w_h = line.split()[0].split('x')
                        w = int(w_h[0])
                        h = int(w_h[1])
                    elif "Position" in line:
                        x_y = line.split()[1].split(',')
                        x = int(x_y[0])
                        y = int(x_y[1])
                        if name is not None and w is not None and h is not None and x is not None and y is not None:
                            outputs_dict[name] = {'name': name,
                                                  'x': x,
                                                  'y': y,
                                                  'width': w,
                                                  'height': h}
        else:
            print("'wlr-randr' command not found, terminating")
            sys.exit(1)

    display = Gdk.Display.get_default()
    for i in range(display.get_n_monitors()):
        monitor = display.get_monitor(i)
        geometry = monitor.get_geometry()

        for key in outputs_dict:
            if int(outputs_dict[key]["x"]) == geometry.x and int(outputs_dict[key]["y"]) == geometry.y:
                outputs_dict[key]["monitor"] = monitor

    return outputs_dict
