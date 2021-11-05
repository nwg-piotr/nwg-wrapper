# nwg-wrapper

This program is a part of the [nwg-shell](https://github.com/nwg-piotr/nwg-shell) project.

This program is a GTK3-based wrapper to display a script output, or a text file content on the desktop in sway or 
other wlroots-based compositors. It uses the [gtk-layer-shell](https://github.com/wmww/gtk-layer-shell) library
to place the window on the bottom layer.

As well the script output, at the text file may be formatted with 
[Pango Markup](https://developer.gnome.org/pygtk/stable/pango-markup-language.html). The window appearance is defined
with css styling. See sample files in the config folder. They also come preinstalled in your `~/.config/nwg-wrapper`
directory. You can find an example of use [at the bottom](https://github.com/nwg-piotr/nwg-wrapper#sample-usage) 
of the page.

[![Packaging status](https://repology.org/badge/vertical-allrepos/nwg-wrapper.svg)](https://repology.org/project/nwg-wrapper/versions)

## Dependencies

- `python` (python3)
- `python-gobject`
- `gtk3`
- `gtk-layer-shell`
- `python-setuptools`
- `python-i3ipc`: for use with sway WM
- `wlr-randr`: for use with other wlroots-based Wayland compositors

## To install

```text
git clone https://github.com/nwg-piotr/nwg-wrapper.git
cd nwg-wrapper
sudo python3 setup.py install --optimize=1
```

## To uninstall

```text
rm -r /usr/lib/python3.9/site-packages/nwg_wrapper*
rm /usr/bin/nwg-wrapper
```

*The path in the first line may be different, depending on your python version.*

## Running

```text
$ nwg-wrapper -h
usage: nwg-wrapper [-h] [-s SCRIPT | -t TEXT] [-c CSS] [-o OUTPUT] [-p POSITION] [-a ALIGNMENT]
                   [-j JUSTIFY] [-mt MARGIN_TOP] [-mb MARGIN_BOTTOM] [-ml MARGIN_LEFT]
                   [-mr MARGIN_RIGHT] [-l LAYER] [-sl SIG_LAYER] [-sv SIG_VISIBILITY] [-r REFRESH]
                   [-v]

optional arguments:
  -h, --help            show this help message and exit
  -s SCRIPT, --script SCRIPT
                        path to the Script whose output you want to display
  -t TEXT, --text TEXT  path to the Text file you want to display
  -c CSS, --css CSS     path to the Css file
  -o OUTPUT, --output OUTPUT
                        Output to place the window on, e.g. "eDP-1"
  -p POSITION, --position POSITION
                        Position: "left" or "right"; "center" if no value given
  -a ALIGNMENT, --alignment ALIGNMENT
                        vertical Alignment: "start" or "end"; "middle" if no value given
  -j JUSTIFY, --justify JUSTIFY
                        text Justification: "right" or "center"; "left" if no value given
  -mt MARGIN_TOP, --margin_top MARGIN_TOP
                        Top Margin
  -mb MARGIN_BOTTOM, --margin_bottom MARGIN_BOTTOM
                        Bottom Margin
  -ml MARGIN_LEFT, --margin_left MARGIN_LEFT
                        Left Margin
  -mr MARGIN_RIGHT, --margin_right MARGIN_RIGHT
                        Right Margin
  -l LAYER, --layer LAYER
                        initial Layer: 1 for bottom, 2 for top; 1 if no value given
  -sl SIG_LAYER, --sig_layer SIG_LAYER
                        Signal number for Layer switching
  -sv SIG_VISIBILITY, --sig_visibility SIG_VISIBILITY
                        Signal number for toggling Visibility
  -r REFRESH, --refresh REFRESH
                        Refresh rate in milliseconds; 0 (no refresh) if no value given
  -v, --version         display version information
```

### Layers

The window will appear on the top or bottom layer, according to the `-l` | `--layer` argument value (1 for bottom by default).
You may switch layers by sending `SIGUSR1` [signal](https://man7.org/linux/man-pages/man7/signal.7.html)
to the `nwg-wrapper` process, e.g. like this:

`pkill -f -10 nwg-wrapper`

or this:

`pkill -f -USR1 nwg-wrapper`

You can choose a different signal number with the `-sl` | `--sig_layer` argument.

### Visibility

The window is visible by default. You can hide / show it by sending `SIGUSR2` signal to the `nwg-wrapper` process:

`pkill -f -12 nwg-wrapper`

or:

`pkill -f -USR2 nwg-wrapper`

You can choose a different signal number with the `-sv | --sig_visibility` argument.

### Sample usage

`nwg-wrapper -s date-wttr.sh -r 1800000 -c date-wttr.css -p left -ml 200`

![2021-07-10-050045_screenshot.png](https://scrot.cloud/images/2021/07/10/2021-07-10-050045_screenshot.png)

`nwg-wrapper -t bindings.pango -c bindings.css -p left -ml 200`

![2021-07-11-003357_screenshot.png](https://scrot.cloud/images/2021/07/11/2021-07-11-003357_screenshot.png)

`nwg-wrapper -s timezones.sh -r 1000 -c timezones.css -p right -mr 50 -a start -mt 50 -j right`

![2021-07-10-050810_screenshot.png](https://scrot.cloud/images/2021/07/10/2021-07-10-050810_screenshot.png)

## (Very basic) image support

nwg-wrapper creates a Gtk.Label widget out of the script output, or the .pango file content. To add an image to it,
we need to pack a Gtk.Image widget before or after the label. To insert an image between the lines of text, the latter 
needs to be divided into more Gtk.Label widgets. Remember to close all Pango tags before adding an image this way.

Syntax:

`#img path=/full/image/path width=int height=int align=string` [start (default) | center | end]

The line is being parsed in the simplest possible way. Spaces are delimiters, so do not use them inside the fields.
It also applies to the file path.

See the [example script](https://github.com/nwg-piotr/nwg-wrapper/blob/img/examples/cowsay.py), and the result below.

![cowsay.png](https://scrot.cloud/images/2021/07/17/cowsay.png)