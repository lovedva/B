#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
# import datetime
# # from gpiozero import PWMLED
# import ina219
# import adt7410
import RPi.GPIO
RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(14, RPi.GPIO.OUT)

try:
    print ("gpio开启")
    # RPi.GPIO.output(14, True)
    while True:
        pass
        RPi.GPIO.output(14, True)
        print ("14==1")
        time.sleep(0.1)
        print ("14==0")
        RPi.GPIO.output(14, False)
        time.sleep(0.1)

        # # ina219.read()
        # print("111")
        # print(adt7410.read_adt7410())



finally:
    RPi.GPIO.cleanup()
