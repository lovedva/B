#!/usr/bin/env python
# -*- coding: utf-8 -*-
import max31855
import time
import pid60Ctr
import pid70Ctr
import pid90Ctr
import sys
import ads1248
import pt1000
import RPi.GPIO
import tty, termios

TempOUT1=14 #60度
TempOUT2=23 #70度
TempOUT3=16 #90度

exitFlag = 0
RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(TempOUT1, RPi.GPIO.OUT)
RPi.GPIO.setup(TempOUT2, RPi.GPIO.OUT)
RPi.GPIO.setup(TempOUT3, RPi.GPIO.OUT)

t0=time.time()
if __name__ == "__main__":
    try:
        pwm1=RPi.GPIO.PWM(TempOUT1,5)#pwm周2500ms
        pwm2=RPi.GPIO.PWM(TempOUT2,5)#pwm周2500ms
        pwm3=RPi.GPIO.PWM(TempOUT3,5)#pwm周2500ms
        pwm1.start(1)
        pwm2.start(1)
        pwm3.start(1)

        pid60=pid60Ctr.pidCtr()
        pid70=pid70Ctr.pidCtr()
        pid90=pid90Ctr.pidCtr()

        file_handle1=open('60Templog.txt',mode='w')
        file_handle2=open('70Templog.txt',mode='w')
        file_handle3=open('90Templog.txt',mode='w')

        ads1248.init()
        RPi.GPIO.output(3,RPi.GPIO.HIGH) #conversation start

        while True:
             # time.sleep(0.05)
             pid60.Pv=float(pt1000.calcTemp(01))
             pid60.calc()
             dc1=pid60.OUT/pid60.pwmcycle*100
             pwm1.ChangeDutyCycle(dc1)

             pid70.Pv=float(pt1000.calcTemp(23))
             pid70.calc()
             dc2=pid70.OUT/pid70.pwmcycle*100
             pwm2.ChangeDutyCycle(dc2)
             thermocouple=max31855.sensor.readTempC()

             pid90.Pv=float(pt1000.calcTemp(45))
             pid90.calc()
             dc3=pid90.OUT/pid90.pwmcycle*100
             pwm3.ChangeDutyCycle(dc3)

             print("Pt1000で測温[01]==%s\n-----------------------------"%pid60.Pv)
             print("Pt1000で測温[23]==%s\n-----------------------------"%pid70.Pv)
             print("----------------------温度センサーで測温[热电偶]："+str(thermocouple))
             print("Pt1000で測温[45]==%s\n-----------------------------"%pid90.Pv)
             file_handle1.write("%s \n"%pid60.Pv)
             file_handle2.write("%s "%pid70.Pv)
             file_handle2.write("| %s \n "%str(thermocouple))
             file_handle3.write("%s \n"%pid90.Pv)

    finally:
        deltaT=time.time()-t0
        print("【--time spent: %s [seconds]--】"%deltaT)
        file_handle1.write("time spent: %ss"%deltaT)
        file_handle1.close()
        file_handle2.close()
        file_handle3.close()
        
        RPi.GPIO.output(3,RPi.GPIO.LOW)
        RPi.GPIO.cleanup()