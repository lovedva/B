#!/bin/sh

#开机启动  sudo nano /etc/profile.d/startup.sh
sleep 2
python3 /home/pi/shabi/piserver/app.py
