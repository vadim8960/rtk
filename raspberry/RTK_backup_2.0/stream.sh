#!/bin/bash

sudo modprobe bcm2835-v4l2
sudo v4l2-ctl --set-fmt-video=width=620,height=480,pixelformat=0

hostname="$1"
hostport="$2"
yellow="\033[33m"
red="\033[31m"

if ["$hostname" = ""]
then
echo -en "${red}Empty hostname \n"
exit
fi

echo -en "${yellow}Streaming to ${hostname}:${hostport} started \n"
sudo raspivid -n -w 640 -h 480 -t 0 -o - | gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay config-interval=10 pt=96 ! udpsink host=${hostname} port=${hostport}
echo -en "${yellow}Streaming stopped \n"
