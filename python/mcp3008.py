#!/usr/bin/env python
# -*- coding: utf-8 -*-
#mcp3008 数模转换 重大注意，硬件spiCE0和CE1用这个类无法输出，需要手动进行高低操作切换，否则无法读取电压。或者使用软件spi
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import time

Vref=3.3
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

if __name__ == '__main__':

	while True:
		adc0 = mcp.read_adc(0)
		adc1=mcp.read_adc(1)
		voltage0 = Vref * (adc0/1023)
		voltage1 = Vref * (adc1/1023)
		print("channel 0 voltage is: ", voltage0)
		print("channel 1 voltage is: ", voltage1)
		time.sleep(0.5)
