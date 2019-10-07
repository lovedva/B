#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import sys
import spidev
import RPi.GPIO
RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(6, RPi.GPIO.OUT)  # start
RPi.GPIO.setup(27, RPi.GPIO.OUT) #reset


class ADS1248:


    MUX0    = 0x00   
    MUX1    = 0x02

    VBIAS   = 0x01
    SYS0    = 0x03

    OFC0    = 0x04
    OFC1    = 0x05
    OFC2    = 0x06

    FSC0    = 0x07
    FSC1    = 0x08
    FSC2    = 0x09

    IDAC0   = 0x0a
    IDAC1   = 0x0b

    GPIOCFG = 0x0c
    GPIODIR = 0x0d
    GPIODAT = 0x0e

    NOP = 0xff
    WREG = 0x40
    RREG = 0x20
    RDATA = 0x12

if __name__ == '__main__':
    try:
        time.sleep(0.02)
        RPi.GPIO.output(6,RPi.GPIO.HIGH)
        spi = spidev.SpiDev()
        spi.open(0,0)

        time.sleep(0.02)
        RPi.GPIO.output(27,RPi.GPIO.LOW)
        time.sleep(0.02)
        RPi.GPIO.output(27,RPi.GPIO.HIGH)

        spi = spidev.SpiDev()
        spi.open(0,0)
        spi.bits_per_word=8
        spi.cshigh=False
        spi.lsbfirst=False
        spi.max_speed_hz=10000
        spi.mode=1
        spi.threewire=False
        
        time.sleep(0.02)
        #MUX0 
        r = spi.xfer2([0b01000000,0b00000000,0b00000001])
        #bias
        r = spi.xfer2([0b01000001,0b00000000,0b00000000])
        #mux1
        r = spi.xfer2([0b01000010,0b00000000,0b00110000])
        #sys0
        r = spi.xfer2([0b01000011,0b00000000,0b00000000])
        #ofc012
        r = spi.xfer2([0b01000100,0b00000000,0b00000000])
        r = spi.xfer2([0b01000101,0b00000000,0b00000000])
        r = spi.xfer2([0b01000110,0b00000000,0b00000000])
        #idac0
        r = spi.xfer2([0b01001010,0b00000000,0b00000110])
        #idac1
        r = spi.xfer2([0b01001011,0b00000000,0b10001011])
        #gpioconfig
        r = spi.xfer2([0b01001100,0b00000000,0b11111111])
        #gpiodirect
        r = spi.xfer2([0b01001101,0b00000000,0b11110111])
        #gpiodat
        r = spi.xfer2([0b01001110,0b00000000,0b00001000])

        while True:
            
            print r
            time.sleep(2)
    except KeyboardInterrupt:
        spi.close() 
        sys.exit(0)
    finally:
        RPi.GPIO.cleanup()  
