'''This entire file is licensed under MIT.
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import argparse
import sys

import gi

gi.require_version('Gtk', '3.0')

try:
    gi.require_version('GtkLayerShell', '0.1')
except ValueError:
    import sys

    raise RuntimeError('\n\n' +
                       'If you haven\'t installed GTK Layer Shell, you need to point Python to the\n' +
                       'library by setting GI_TYPELIB_PATH and LD_LIBRARY_PATH to <build-dir>/src/.\n' +
                       'For example you might need to run:\n\n' +
                       'GI_TYPELIB_PATH=build/src LD_LIBRARY_PATH=build/src python3 ' + ' '.join(sys.argv))

from gi.repository import Gtk, GtkLayerShell


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s",
                        "--script",
                        type=str,
                        default="",
                        help="Path to the script whose output you want to display")

    parser.add_argument("-c",
                        "--css",
                        type=str,
                        default="",
                        help="Path to the css file")

    parser.add_argument("-o",
                        "--output",
                        type=str,
                        default="",
                        help="Output to place the window on, e.g. \"eDP-1\"")

    parser.add_argument("-p",
                        "--position",
                        type=str,
                        help="Position: \"bottom\", \"top\", \"left\" or \"right\"; \"center\" if no value given")

    parser.add_argument("-f",
                        "--fullscreen",
                        type=bool,
                        help="Take full window width/height")

    parser.add_argument("-a",
                        "--alignment",
                        type=str,
                        help="Alignment in full width/height: \"start\" or \"end\"; \"middle\" if no value given")

    parser.add_argument("-mt",
                        "--margin_top",
                        type=int,
                        help="Top margin")

    parser.add_argument("-mb",
                        "--margin_bottom",
                        type=int,
                        help="Bottom margin")

    parser.add_argument("-ml",
                        "--margin_left",
                        type=int,
                        help="Left margin")

    parser.add_argument("-mr",
                        "--margin_right",
                        type=int,
                        help="Right margin")

    args = parser.parse_args()

    window = Gtk.Window()
    label = Gtk.Label(label='GTK Layer Shell with Python!')
    window.add(label)

    GtkLayerShell.init_for_window(window)
    GtkLayerShell.set_layer(window, GtkLayerShell.Layer.BOTTOM)
    GtkLayerShell.set_margin(window, GtkLayerShell.Edge.TOP, 10)
    GtkLayerShell.set_margin(window, GtkLayerShell.Edge.BOTTOM, 50)
    GtkLayerShell.set_anchor(window, GtkLayerShell.Edge.BOTTOM, 1)

    window.show_all()
    window.connect('destroy', Gtk.main_quit)
    Gtk.main()


if __name__ == "__main__":
    sys.exit(main())
