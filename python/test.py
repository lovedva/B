#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
from gpiozero import PWMLED
import ina219
import adt7410

# led2 = PWMLED(12)
# led2.on()
# print ("gpio开启")


while True:
    time.sleep(0.5)
    ina219.read()
    print("")
    print(adt7410.read_adt7410())


