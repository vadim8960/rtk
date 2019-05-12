#!/bin/bash

pkill -9 python

sudo python3 client_gamepad.py &
python3 client_video.py 
