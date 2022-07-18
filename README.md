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
rm -r /usr/lib/python3.*/site-packages/nwg_wrapper*
rm /usr/bin/nwg-wrapper
```

*The path in the first line may be different, depending on your python version.*

## Running

```text
$ nwg-wrapper -h
usage: nwg-wrapper [-h] [-s SCRIPT | -t TEXT] [-c CSS] [-o OUTPUT] [-p POSITION] [-a ALIGNMENT] [-j JUSTIFY]
                   [-mt MARGIN_TOP] [-mb MARGIN_BOTTOM] [-ml MARGIN_LEFT] [-mr MARGIN_RIGHT] [-l LAYER]
                   [-sl SIG_LAYER] [-sv SIG_VISIBILITY] [-sq SIG_QUIT] [-r REFRESH] [-v]

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
  -i, --invisible
                        Make this instance of wrapper invisible on launch
  -sl SIG_LAYER, --sig_layer SIG_LAYER
                        Signal number for Layer switching; default: 10
  -sv SIG_VISIBILITY, --sig_visibility SIG_VISIBILITY
                        Signal number for toggling Visibility; default: 12
  -sq SIG_QUIT, --sig_quit SIG_QUIT
                        custom Signal number to Quit the wrapper instance; default: 2
  -r REFRESH, --refresh REFRESH
                        Refresh rate in milliseconds; 0 (no refresh) if no value given
  -v, --version         display version information
```

### Layers

The window will appear on the top or bottom layer, according to the `-l` | `--layer` argument value (1 for bottom by 
default, 2 for top). You may bring it to the overlay layer (3) and back to the layer you selected by sending `SIGUSR1` 
[signal](https://man7.org/linux/man-pages/man7/signal.7.html) to the `nwg-wrapper` process, e.g. like this:

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

Also, you can hide it on start with `-i` | `--invisible` argument and then show and hide it, using your specified or `USR2` signal.

### Custom quit signal

Sometimes you may need to terminate a certain nwg-wrapper instance (see [#5](https://github.com/nwg-piotr/nwg-wrapper/issues/5)).
You may choose a custom signal with the `-sq` | `--sig_quit` argument.

Sample script to show the wrapper over swaylock and kill it when the screen gets unlocked, w/o killing other instances:

```bash
#!/bin/bash

nwg-wrapper -s swaylock-time.sh -o eDP-1 -r 1000 -c timezones.css -p right -mr 50 -a start -mt 0 -j right -l 3 -sq 31 &
sleep 0.5 && swaylock --image '/home/piotr/Obrazy/Wallpapers/wallhaven-zmrdry-1920x1080.jpg' && pkill -f -31 nwg-wrapper
```

*Note: You may need a different `sleep` value on various machines, e.g. `sleep 1`. 
See: https://github.com/nwg-piotr/nwg-wrapper/issues/19*

### Sample usage

`nwg-wrapper -s date-wttr.sh -r 1800000 -c date-wttr.css -p left -ml 200`

![screenshot-1.png](https://raw.githubusercontent.com/nwg-piotr/nwg-shell-resources/master/images/nwg-wrapper/timezones.png)

`nwg-wrapper -t bindings.pango -c bindings.css -p left -ml 200`

![screenshot-2.png](https://raw.githubusercontent.com/nwg-piotr/nwg-shell-resources/master/images/nwg-wrapper/weather.png)

`nwg-wrapper -s timezones.sh -r 1000 -c timezones.css -p right -mr 50 -a start -mt 50 -j right`

![screenshot-3.png](https://raw.githubusercontent.com/nwg-piotr/nwg-shell-resources/master/images/nwg-wrapper/bindings.png)

## (Very basic) image support

nwg-wrapper creates a Gtk.Label widget out of the script output, or the .pango file content. To add an image to it,
we need to pack a Gtk.Image widget before or after the label. To insert an image between the lines of text, the latter 
needs to be divided into more Gtk.Label widgets. Remember to close all Pango tags before adding an image this way.

Syntax:

`#img path='/full/path/to/your image.png' width=int height=int align=string` [start (default) | center | end]

See the [example script](https://github.com/nwg-piotr/nwg-wrapper/blob/master/examples/cowsay.py), and the result below.

![cowsay.png](https://raw.githubusercontent.com/nwg-piotr/nwg-shell-resources/master/images/nwg-wrapper/cowsay.png)
