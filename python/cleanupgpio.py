#!/usr/bin/python
# -*- coding: UTF-8 -*-
import RPi.GPIO


TempOUT1=12 #60度
TempOUT2=23 #70度
TempOUT3=15 #90度
RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(TempOUT1, RPi.GPIO.OUT)
RPi.GPIO.setup(TempOUT2, RPi.GPIO.OUT)
RPi.GPIO.setup(TempOUT3, RPi.GPIO.OUT)
try:
    print("cleanup gpio...") 
    while True  :
        pass
finally:
    RPi.GPIO.cleanup()