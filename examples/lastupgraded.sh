#!/usr/bin/env bash

title="Last Upgrade:"
color="#a1d4c7"
pattern="$(tail -n1 /var/log/pacman.log | grep -iEo "([0-9]{4}-[0-9]{2}-[0-9]{2})").+(upgraded|installed)"
cmd=$(grep -aiE "$pattern" /var/log/pacman.log|cut -d' ' -f4|sort -u)
textfont="Fixedsys Excelsior MonoL"
# fontsize="6pt"
source ~/.config/nwg-wrapper/termout.sh

