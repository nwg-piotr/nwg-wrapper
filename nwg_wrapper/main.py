#!/usr/bin/env python3

'''This entire file is licensed under MIT.
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import argparse
import sys

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

from gi.repository import Gtk, Gdk, GLib, GtkLayerShell

from tools import *

dir_name = os.path.dirname(__file__)
inner_box_width = 0
inner_box = Gtk.Box()


def update_label_from_script(path, label):
    try:
        output = subprocess.check_output(path).decode("utf-8")[:-1]
    except Exception as e:
        output = '<span size="large" foreground="#ff0000">\nERROR:</span>\n\n<i>{}</i> '.format(e)
        print(e)
    label.set_label(output)
    set_box_width()

    return True


def update_label_from_text(path, label):
    try:
        with open(path, 'r') as file:
            output = file.read()
    except Exception as e:
        output = '<span size="large" foreground="#ff0000">\nERROR:</span>\n\n<i>{}</i> not found\n'.format(path)
        print(e)
    label.set_label(output)
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
                       help="Path to the script whose output you want to display")

    group.add_argument("-t",
                       "--text",
                       type=str,
                       default="",
                       help="Path to the text file you want to display")

    parser.add_argument("-c",
                        "--css",
                        type=str,
                        default="style.css",
                        help="Path to the css file")

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
                        help="Vertical alignment: \"start\" or \"end\"; \"middle\" if no value given")

    parser.add_argument("-j",
                        "--justify",
                        type=str,
                        help="Text justification: \"right\" or \"center\"; \"left\" if no value given")

    parser.add_argument("-mt",
                        "--margin_top",
                        type=int,
                        default=0,
                        help="Top margin")

    parser.add_argument("-mb",
                        "--margin_bottom",
                        type=int,
                        default=0,
                        help="Bottom margin")

    parser.add_argument("-ml",
                        "--margin_left",
                        type=int,
                        default=0,
                        help="Left margin")

    parser.add_argument("-mr",
                        "--margin_right",
                        type=int,
                        default=0,
                        help="Right margin")

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

    args = parser.parse_args()

    config_dir = get_config_dir()
    # Only if not found
    copy_files(os.path.join(dir_name, "config"), config_dir)

    screen = Gdk.Screen.get_default()
    provider = Gtk.CssProvider()
    style_context = Gtk.StyleContext()
    style_context.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
    try:
        file = os.path.join(config_dir, args.css)
        provider.load_from_path(file)
        print("Using style: {}".format(file))
    except:
        print("ERROR: {} file not found, using GTK styling".format(os.path.join(config_dir, args.css)))

    window = Gtk.Window()

    GtkLayerShell.init_for_window(window)
    GtkLayerShell.set_layer(window, GtkLayerShell.Layer.BOTTOM)
    GtkLayerShell.set_exclusive_zone(window, 0)

    if args.output:
        outputs = list_outputs()
        try:
            monitor = outputs[args.output]["monitor"]
            GtkLayerShell.set_monitor(window, monitor)
        except KeyError:
            print("No such output: {}".format(args.output))

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

    label = Gtk.Label()
    label.set_use_markup(True)
    if args.justify:
        if args.justify == "right":
            label.set_justify(Gtk.Justification.RIGHT)
        elif args.justify == "center":
            label.set_justify(Gtk.Justification.CENTER)
        else:
            label.set_justify(Gtk.Justification.LEFT)

    # Get data
    script_path = os.path.join(config_dir, args.script) if args.script else ""
    text_path = os.path.join(config_dir, args.text) if args.text else ""

    if script_path:
        print("Using script: {}".format(script_path))
        update_label_from_script(script_path, label)
    elif text_path:
        print("Using text file: {}".format(text_path))
        update_label_from_text(text_path, label)
    else:
        print("Neither script nor text file specified")

    inner_box.pack_start(label, False, False, 0)

    window.show_all()
    window.connect('destroy', Gtk.main_quit)

    if script_path and args.refresh > 0:
        GLib.timeout_add(args.refresh, update_label_from_script, script_path, label)

    Gtk.main()


if __name__ == "__main__":
    sys.exit(main())
