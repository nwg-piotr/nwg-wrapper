#!/usr/bin/env bash

title="Systemd Timers:"
color="#8cc7d6"
cmd="$(systemctl --user list-timers|head -n -1)"
textfont="Fixedsys Excelsior MonoL"
# fontsize="11pt"
source ~/.config/nwg-wrapper/termout.sh

