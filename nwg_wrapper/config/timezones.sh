#!/usr/bin/env bash

# Most of the countries below have more than one time zone,
# and it makes sense to use cities instead of countries!
# Use tzselect to find their time zones.

time=$(TZ='America/Fortaleza' date +'%H:%M:%S')
echo '<span size="25000" foreground="#998000" face="monospace" weight="bold">Brazil '$time'</span>'

echo '<span size="x-large" face="monospace" foreground="#ccc">'
time=$(TZ='America/Vancouver' date +"%H:%M")
echo 'Canada\t<b>'$time'</b>'

time=$(TZ='Europe/Dublin' date +"%H:%M")
echo 'Ireland\t<b>'$time'</b>'

time=$(TZ='Asia/Kolkata' date +"%H:%M")
echo 'India\t<b>'$time'</b>'

time=$(TZ='Asia/Shanghai' date +"%H:%M")
echo 'China\t<b>'$time'</b>'
echo '</span>'