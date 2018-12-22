#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
from gpiozero import PWMLED

led2 = PWMLED(12)

led1 = PWMLED(6)
led1.on()
led2.on()
# time.sleep(3)
# led.off()
print ("gpio开启")
a=2.234
b=5.3432
c=a*b 
print (c)
while True:
	pass
