#!/usr/bin/env python
# -*- coding: utf-8 -*-
#mcp3008 数模转换 重大注意，硬件spiCE0和CE1用这个类无法输出，需要手动进行高低操作切换，否则无法读取电压。或者使用软件spi
#https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008  使用的python库
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import time

Vref=3.3
CLK  = 26
MISO = 20
MOSI = 10
CS   = 27
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

if __name__ == '__main__':
    print("Mcp3008，c0=0 c1=1")
    while True:
        adc0 = mcp.read_adc(0)
        print(adc0)
        adc1=mcp.read_adc(1)
        print(adc1)

        voltage0 = Vref * (adc0/1023.0000)
        voltage1 = Vref * (adc1/1023.0000)
        print("channel 0 voltage is: ", voltage0)
        print("channel 1 voltage is: ", voltage1)
        time.sleep(1)
