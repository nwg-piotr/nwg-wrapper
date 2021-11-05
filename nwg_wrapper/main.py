#!/usr/bin/env python3

"""
Wrapper to display a script output or a text file content on the desktop in sway or other wlroots-based compositors
Author: Piotr Miller
e-mail: nwg.piotr@gmail.com
Project: https://github.com/nwg-piotr/nwg-wratter
License: MIT
"""

import argparse
import sys
import signal

from nwg_wrapper.__about__ import __version__

import gi
gi.require_version('Gtk', '3.0')
try:
    gi.require_version('GtkLayerShell', '0.1')
except ValueError:
    raise RuntimeError('\n\n' +
                       'If you haven\'t installed GTK Layer Shell, you need to point Python to the\n' +
                       'library by setting GI_TYPELIB_PATH and LD_LIBRARY_PATH to <build-dir>/src/.\n' +
                       'For example you might need to run:\n\n' +
                       'GI_TYPELIB_PATH=build/src LD_LIBRARY_PATH=build/src python3 ' + ' '.join(sys.argv))

from gi.repository import GLib, GtkLayerShell

from nwg_wrapper.tools import *

dir_name = os.path.dirname(__file__)
inner_box_width = 0
inner_box = Gtk.Box()
window = None
layer = 1
args = None


def signal_handler(sig, frame):
    global layer
    if sig == 2 or sig == 15:
        desc = {2: "SIGINT", 15: "SIGTERM"}
        print("Terminated with {}".format(desc[sig]))
        Gtk.main_quit()
    elif sig == args.sig_layer:
        layer = 1 if layer == 2 else 2
        GtkLayerShell.set_layer(window, layer)
    elif sig == args.sig_visibility:
        if window.is_visible():
            window.hide()
        else:
            window.show_all()


def update_label_from_script(path, v_box, justify):
    for item in v_box.get_children():
        item.destroy()
    try:
        output = subprocess.check_output(path).decode("utf-8")[:-1]
    except Exception as e:
        output = '<span size="large" foreground="#ff0000">\nERROR:</span>\n\n<i>{}</i> '.format(e)
        sys.stderr.write("{}\n".format(e))

    content = parse_output(output, justify)
    for item in content:
        h_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        v_box.pack_start(h_box, False, False, 0)
        if isinstance(item, AlignedImage):
            if item.align == "end":
                h_box.pack_end(item, False, False, 0)
            elif item.align != "center":
                h_box.pack_start(item, False, False, 0)
            else:
                h_box.pack_start(item, True, True, 0)
        else:
            h_box.pack_start(item, True, True, 0)

    v_box.show_all()
    set_box_width()

    return True


def build_from_text(path, v_box, justify):
    try:
        with open(path, 'r') as file:
            output = file.read()
    except Exception as e:
        output = '<span size="large" foreground="#ff0000">\nERROR:</span>\n\n<i>{}</i> not found\n'.format(path)
        sys.stderr.write("{}\n".format(e))

    content = parse_output(output, justify)
    for item in content:
        h_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        h_box.set_property("name", "test")
        v_box.pack_start(h_box, False, False, 0)
        if isinstance(item, AlignedImage):
            if item.align == "end":
                h_box.pack_end(item, False, False, 0)
            elif item.align != "center":
                h_box.pack_start(item, False, False, 0)
            else:
                h_box.pack_start(item, True, True, 0)
        else:
            h_box.pack_start(item, True, True, 0)

    set_box_width()

    return True


# remember max box width to minimize floating when content length changes
def set_box_width():
    global inner_box, inner_box_width
    w = inner_box.get_allocated_width()
    if w > inner_box_width:
        inner_box.set_size_request(w, 0)
        inner_box_width = w


def main():
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-s",
                       "--script",
                       type=str,
                       default="",
                       help="path to the Script whose output you want to display")

    group.add_argument("-t",
                       "--text",
                       type=str,
                       default="",
                       help="path to the Text file you want to display")

    parser.add_argument("-c",
                        "--css",
                        type=str,
                        default="style.css",
                        help="path to the Css file")

    parser.add_argument("-o",
                        "--output",
                        type=str,
                        default="",
                        help="Output to place the window on, e.g. \"eDP-1\"")

    parser.add_argument("-p",
                        "--position",
                        type=str,
                        help="Position: \"left\" or \"right\"; \"center\" if no value given")

    parser.add_argument("-a",
                        "--alignment",
                        type=str,
                        help="vertical Alignment: \"start\" or \"end\"; \"middle\" if no value given")

    parser.add_argument("-j",
                        "--justify",
                        type=str,
                        default="left",
                        help="text Justification: \"right\" or \"center\"; \"left\" if no value given")

    parser.add_argument("-mt",
                        "--margin_top",
                        type=int,
                        default=0,
                        help="Top Margin")

    parser.add_argument("-mb",
                        "--margin_bottom",
                        type=int,
                        default=0,
                        help="Bottom Margin")

    parser.add_argument("-ml",
                        "--margin_left",
                        type=int,
                        default=0,
                        help="Left Margin")

    parser.add_argument("-mr",
                        "--margin_right",
                        type=int,
                        default=0,
                        help="Right Margin")

    parser.add_argument("-l",
                        "--layer",
                        type=int,
                        default=1,
                        help="initial Layer: 1 for bottom, 2 for top; 1 if no value given")

    parser.add_argument("-sl",
                        "--sig_layer",
                        type=int,
                        default=10,
                        help="Signal number for Layer switching")

    parser.add_argument("-sv",
                        "--sig_visibility",
                        type=int,
                        default=12,
                        help="Signal number for toggling Visibility ")

    parser.add_argument("-r",
                        "--refresh",
                        type=int,
                        default=0,
                        help="Refresh rate in milliseconds; 0 (no refresh) if no value given")

    parser.add_argument("-v",
                        "--version",
                        action="version",
                        version="%(prog)s version {}".format(__version__),
                        help="display version information")

    global args
    args = parser.parse_args()

    global layer
    layer = args.layer

    if not args.text and not args.script:
        sys.stderr.write("ERROR: Neither script nor text file specified\n")
        parser.print_help(sys.stderr)
        sys.exit(1)

    config_dir = get_config_dir()
    # Only if not found
    copy_files(os.path.join(dir_name, "config"), config_dir)

    global window
    window = Gtk.Window()

    GtkLayerShell.init_for_window(window)
    GtkLayerShell.set_layer(window, args.layer)
    GtkLayerShell.set_exclusive_zone(window, 0)

    if args.output:
        outputs = list_outputs()
        try:
            monitor = outputs[args.output]["monitor"]
            GtkLayerShell.set_monitor(window, monitor)
        except KeyError:
            print("No such output: {}".format(args.output))

    screen = Gdk.Screen.get_default()
    provider = Gtk.CssProvider()
    style_context = Gtk.StyleContext()
    style_context.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
    try:
        file = os.path.join(config_dir, args.css)
        provider.load_from_path(file)
        print("Using style: {}".format(file))
    except:
        sys.stderr.write("ERROR: {} file not found, using GTK styling\n".format(os.path.join(config_dir, args.css)))

    if args.position == "left" or args.position == "right":
        if args.position == "left":
            GtkLayerShell.set_anchor(window, GtkLayerShell.Edge.LEFT, True)
        else:
            GtkLayerShell.set_anchor(window, GtkLayerShell.Edge.RIGHT, True)

    GtkLayerShell.set_anchor(window, GtkLayerShell.Edge.TOP, True)
    GtkLayerShell.set_anchor(window, GtkLayerShell.Edge.BOTTOM, True)

    GtkLayerShell.set_margin(window, GtkLayerShell.Edge.TOP, args.margin_top)
    GtkLayerShell.set_margin(window, GtkLayerShell.Edge.BOTTOM, args.margin_bottom)
    GtkLayerShell.set_margin(window, GtkLayerShell.Edge.LEFT, args.margin_left)
    GtkLayerShell.set_margin(window, GtkLayerShell.Edge.RIGHT, args.margin_right)

    outer_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    outer_box.set_property("name", "box-outer")
    window.add(outer_box)

    inner_box.set_orientation(Gtk.Orientation.HORIZONTAL)
    inner_box.set_property("name", "box-inner")
    if args.alignment == "start":
        outer_box.pack_start(inner_box, False, True, 0)
    elif args.alignment == "end":
        outer_box.pack_end(inner_box, False, True, 0)
    else:
        outer_box.pack_start(inner_box, True, False, 0)

    v_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    inner_box.pack_start(v_box, False, False, 0)

    # Get data
    script_path = os.path.join(config_dir, args.script) if args.script else ""
    text_path = os.path.join(config_dir, args.text) if args.text else ""

    if script_path:
        r = "refresh rate {} ms".format(args.refresh) if args.refresh else "no refresh"
        print("Using script: {}, {}".format(script_path, r))
        update_label_from_script(script_path, v_box, args.justify)
    elif text_path:
        print("Using text file: {}".format(text_path))
        build_from_text(text_path, v_box, args.justify)

    window.show_all()
    window.connect('destroy', Gtk.main_quit)

    if script_path and args.refresh > 0:
        GLib.timeout_add(args.refresh, update_label_from_script, script_path, v_box, args.justify)

    catchable_sigs = set(signal.Signals) - {signal.SIGKILL, signal.SIGSTOP}
    for sig in catchable_sigs:
        signal.signal(sig, signal_handler)

    Gtk.main()


if __name__ == "__main__":
    sys.exit(main())
