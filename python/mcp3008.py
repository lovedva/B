#!/usr/bin/env python
# -*- coding: utf-8 -*-
#AD转换 10位 mcp3008
from gpiozero import MCP3008
import time

from gpiozero import MCP3008
from time import sleep
voltage = [0,0,0,0,0,0,0,0]
vref = 3.3
while True:
    for x in range(0, 8):
        with MCP3008(channel=x) as reading:
            voltage[x] = reading.value * vref
        print(x,": ", voltage[x])
    sleep(1)

