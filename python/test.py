#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
# import datetime
# # from gpiozero import PWMLED
# import ina219
# import adt7410
import RPi.GPIO
RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(5, RPi.GPIO.OUT)

try:
    RPi.GPIO.output(5, True)
    print ("gpio开启")


    while True:
        time.sleep(0.5)
        # ina219.read()
        print("111")
        # print(adt7410.read_adt7410())

finally:
    RPi.GPIO.cleanup()
