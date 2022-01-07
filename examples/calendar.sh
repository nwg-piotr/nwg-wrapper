#!/usr/bin/env bash

title="Today:"
color="#8EA6D6"
fontsize="12pt"
cmd="$(khal --color calendar 2>/dev/null)"
source ~/.config/nwg-wrapper/termout.sh
