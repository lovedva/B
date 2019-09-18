#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import sys
import spidev

spi = spidev.SpiDev()
spi.open(0,0)

def readAdc(channel):
    if ((channel > 7) or (channel < 0)):
        return -1
    # r = spi.xfer2([0x01,0x08|(channel<<4),0])
    r = spi.xfer2([0b00000001,0b00001000|(channel<<4),0])
    # byte2 = (r[1] & 0x03)
    byte2 = (r[1] & 0b0000011)
    return (byte2 << 8) | r[2]

if __name__ == '__main__':
    try:
        while True:
            val = readAdc(0)
            print "ADC Result: ", str(val)
            time.sleep(1)
    except KeyboardInterrupt:
        spi.close() 
        sys.exit(0)
