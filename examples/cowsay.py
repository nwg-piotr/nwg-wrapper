#!/usr/bin/env python3
"""
Example usage of the #img tag
The simplest way is to add an image at the beginning or the end of the script. If you need it somewhere inside,
you must close all open Pango tags first.

#img path=string width=int height=int align=string [start (default) | center | end]

" and ' signs are ignored. Space is the delimiter, so you must not use it inside fields (applies to the file path!)

For the script to work, you need `fortune` and `cowsay` packages
"""
import subprocess
import os
import sys


def get_output(command):
    try:
        output = subprocess.check_output(command, shell=True).decode("utf-8").strip()
    except Exception as e:
        output = e
        sys.stderr.write("{}\n".format(e))

    return output


def main():
    time = get_output("LC_ALL=C TZ='Europe/Warsaw' date +'%A, %d. %B'")
    wttr = get_output("curl https://wttr.in/?format=1")
    print('<span size="35000" foreground="#998000">{}</span><span size="30000" foreground="#ccc">'.format(time))
    print('{}</span>'.format(wttr))
    uname = os.getenv("USER")
    host = get_output("uname -n")
    kernel = get_output("uname -sr")
    print('<span foreground="#aaa">{}@{} {}'.format(uname, host, kernel))
    print(get_output("sway -v"))
    print('</span>')
    try:
        print('<span font_family="monospace" foreground="#ccc">')
        cow = get_output("fortune | cowsay")
        # "<" and ">" would be interpreted as parts of Pango markup
        cow = cow.replace("<", "{")
        cow = cow.replace(">", "}")
        print(cow)
        print('</span>')
    except Exception as e:
        print("cow is dead: {}".format(e))

    # place your image path here
    print('#img path=/home/piotr/Obrazy/grass.png width=430 height=70')


if __name__ == '__main__':
    main()
