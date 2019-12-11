#!/usr/bin/env python
# -*- coding: utf-8 -*-
#data sheet http://www.ti.com/cn/lit/ds/symlink/ads1247.pdf
import time
import sys
import spidev
import RPi.GPIO

RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(6, RPi.GPIO.OUT)  # start
RPi.GPIO.setup(3, RPi.GPIO.OUT) #reset

time.sleep(0.02)
RPi.GPIO.output(6,RPi.GPIO.HIGH)
spi = spidev.SpiDev()
spi.open(0,0)

time.sleep(0.02)
RPi.GPIO.output(3,RPi.GPIO.LOW)
time.sleep(0.02)
RPi.GPIO.output(3,RPi.GPIO.HIGH)

spi = spidev.SpiDev()
spi.open(0,0)
spi.bits_per_word=8
spi.cshigh=False
spi.lsbfirst=False
spi.max_speed_hz=10000
spi.mode=1
spi.threewire=False
time.sleep(0.1)

#初始化
 
def init():
    #MUX0
    r = spi.xfer2([0b01000000,0b00000000,0b00000001])
    #mux1
    r = spi.xfer2([0b01000010,0b00000000,0b00100000])
    #sys0
    r = spi.xfer2([0b01000011,0b00000000,0b00000000])
    #idac0
    r = spi.xfer2([0b01001010,0b00000000,0b00000110])
    #idac1
    r = spi.xfer2([0b01001011,0b00000000,0b10001011]) 
    #bias
    r = spi.xfer2([0b01000001,0b00000000,0b00000000])
    #ofc012
    r = spi.xfer2([0b01000100,0b00000000,0b00000000])
    r = spi.xfer2([0b01000101,0b00000000,0b00000000])
    r = spi.xfer2([0b01000110,0b00000000,0b00000000])
 
    #gpioconfig
    r = spi.xfer2([0b01001100,0b00000000,0b11111100])
    #gpiodirect
    r = spi.xfer2([0b01001101,0b00000000,0b11111100])
    #gpiodat
    r = spi.xfer2([0b01001110,0b00000000,0b00000000])
    spi.xfer2([0b00010110]) #停止模式 Rdata读取
    print("init completed")

def voltcalc(r):
    V=(r[0]<<16)+(r[1]<<8)+r[2]
    print(V)
    volts=1.0*V/(pow(2,23)-1)*2.011 #Refernce volt 2.045
    return volts

def readAdcChannel(channel): #ain0+ ain1-  2+3- 4+5-
    if channel==01:
        spi.xfer2([0b01000000,0b00000000,0b00000001])
        time.sleep(0.25)
        spi.xfer2([0b00010010,])
        r0=spi.xfer2([0xff,0xff,0xff])
        # print r0
        volts0=voltcalc(r0)
        print ("U[AIN0+ Ain1-] = %s V"%(volts0)) 
        return volts0
    elif channel==23:
        spi.xfer2([0b01000000,0b00000000,0b00010011])
        time.sleep(0.25)
        spi.xfer2([0b00010010,])
        r1=spi.xfer2([0xff,0xff,0xff])
        # print r1
        volts1=voltcalc(r1)
        print ("U[AIN2+ Ain3-] = %s V"%(volts1))  
        return volts1
    elif channel==45:
        spi.xfer2([0b01000000,0b00000000,0b00100101])
        time.sleep(0.25)
        spi.xfer2([0b00010010,])
        r2=spi.xfer2([0xff,0xff,0xff])
        # print r2
        volts2=voltcalc(r2)
        print ("U[AIN4+ Ain5-] = %s V"%(volts2))
        return volts2
    elif channel==67:
        spi.xfer2([0b01000000,0b00000000,0b00110111])
        time.sleep(0.25)
        spi.xfer2([0b00010010,])
        r2=spi.xfer2([0xff,0xff,0xff])
        # print r2
        volts3=voltcalc(r2)
        print ("U[AIN6+ Ain7-] = %s V"%(volts3))
        return volts3
    else:
        print("请传递正确的通道参数")


if __name__ == '__main__':
    try:
        init()
        RPi.GPIO.output(3,RPi.GPIO.HIGH)
        file_handle1=open('ads1248log.txt',mode='w')
        flag=0
        while True:   
            
            # v1 = readAdcChannel(23)
            # v2 = readAdcChannel(45)
            sum=0
            for i in range(0,4):
                
                v0 = readAdcChannel(01)
                sum=sum+v0
                
                # flag=flag+1

            avg=sum/4
            print("avg==%s"%avg)
            flag=flag+1
            print("flag==%s"%flag)
            file_handle1.write("%s \n"%avg)
                


    except KeyboardInterrupt:
        spi.close() 
        sys.exit(0)
    finally:
        RPi.GPIO.output(3,RPi.GPIO.LOW)
        RPi.GPIO.cleanup()  
        file_handle1.close()
