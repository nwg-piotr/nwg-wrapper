#!/usr/bin/env bash

# Most of the countries below have more than one time zone,
# and it makes sense to use cities instead of countries!
# Use tzselect to find their time zones.

time=$(TZ='America/Fortaleza' date +"%H:%M")
echo '<span size="large">Brazil</span>\t<b>'$time'</b>'

time=$(TZ='America/Vancouver' date +"%H:%M")
echo '<span size="large">Canada</span>\t<b>'$time'</b>'

time=$(TZ='Europe/Dublin' date +"%H:%M")
echo '<span size="large">Ireland</span>\t<b>'$time'</b>'

time=$(TZ='Asia/Kolkata' date +"%H:%M")
echo '<span size="large">India</span>\t<b>'$time'</b>'

time=$(TZ='Asia/Shanghai' date +"%H:%M")
echo '<span size="large">China</span>\t<b>'$time'</b>'