#!/usr/bin/env bash

time=$(LC_ALL=C TZ='Europe/Warsaw' date +'%A, %d. %B  %H:%M')
wttr=$(curl https://wttr.in/?format=1)
echo '<span size="25000" foreground="#998000">'$time'</span><span size="20000" foreground="#ccc">'
echo $wttr'</span>'