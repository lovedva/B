#!/usr/bin/env python
# -*- coding: utf-8 -*-
#mcp3008 数模转换
from gpiozero import MCP3008

Vref=5.06

adc0 = MCP3008(channel=0)
adc1=MCP3008(channel=1)
voltage0 = Vref * adc0.value
voltage1 = Vref * adc1.value
print("channel 0 voltage is: ", voltage0)
print("channel 1 voltage is: ", voltage1)
