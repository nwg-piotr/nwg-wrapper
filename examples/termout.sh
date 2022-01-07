#!/usr/bin/env bash

title=${title:-"Output"}
cmd=${cmd:-"I am empty"}
color=${color:-"#C88FAF"}
titlefont=${titlefont:-"SF Pro Display"}
textfont=${textfont:-"SF Mono"}
fontsize=${fontsize:-"10pt"}
# cmd
# color
#ansifilter the cmd output to pango markup.
cmd=$(ansifilter -c -M -F "$textfont" -s $fontsize -m ~/.config/nwg-wrapper/ansicolor.map --art-tundra <<< "$cmd"|sed "s/fgcolor=\"#000000\" bgcolor=\"#000000\"/bgcolor=\"#FFFFFF20\" fgcolor=\"$color\"/g")
cat - << DOC
<span foreground="$color" font_family="$titlefont" size="xx-large">$title</span>

<span foreground="$color" font_family="$textfont" >$cmd</span>
DOC

# echo -e " "

