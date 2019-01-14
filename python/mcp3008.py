#!/usr/bin/env python
# -*- coding: utf-8 -*-
#mcp3008 数模转换
from gpiozero import MCP3008
import time

Vref=3.3

adc0 = MCP3008(0)
adc1=MCP3008(1)
while True:
	voltage0 = Vref * adc0.value
	voltage1 = Vref * adc1.value
	print("channel 0 voltage is: ", voltage0)
	print("channel 1 voltage is: ", voltage1)
	time.sleep(0.5)
