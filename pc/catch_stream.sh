#!/bin/bash

sudo gst-launch-1.0 -v udpsrc port=9000 caps='application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264' ! rtph264depay ! video/x-h264,width=640,height=480,framerate=30/1 ! h264parse ! avdec_h264 ! videoconvert ! autovideosink sync=false
