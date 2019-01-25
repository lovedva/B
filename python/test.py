#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
from gpiozero import PWMLED

led2 = PWMLED(12)

#led1 = PWMLED(27)
#ed1.on()
led2.on()
# time.sleep(3)
# led.off()
print ("gpio开启")

while True:
	pass
