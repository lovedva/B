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
    pwm1=RPi.GPIO.PWM(14,90)
    pwm1.start(1)
    pwm1.ChangeDutyCycle(50.0)
    while True:
        pass
        # RPi.GPIO.output(14, True)
        # time.sleep(5)
        # RPi.GPIO.output(14, False)
        # time.sleep(5)
        # # ina219.read()
        # print("111")
        # print(adt7410.read_adt7410())



finally:
    RPi.GPIO.cleanup()
