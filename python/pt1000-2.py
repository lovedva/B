#!/usr/bin/env python
# -*- coding: utf-8 -*-
#pt1000温度测定，数模转换mcp3008
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import time
import numpy as np
import adt7410
# from gpiozero import PWMLED

Vref=3.31 #V
I=0.001 #A （平均值）
# led = PWMLED(12)  #供电端口 gpio12
CLK  = 15
MISO = 13
MOSI = 19
CS   = 12
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

def calcResistance(channel1,channel2):
    adc0 = mcp.read_adc(channel1)
    adc1=mcp.read_adc(channel2)
    voltage0 = Vref * (adc0/1023.000)
    voltage1 = Vref * (adc1/1023.000)
    
    print("channel 0 voltage is: ", voltage0)
    print("channel 1 voltage is: ", voltage1)
    print("Pt1000's resistance now is: ",(voltage1-voltage0)/I)

    return (voltage1-voltage0)/I #单位欧姆

def calcTemp(a,b,c):
    if a == 0:
        print('您输入的不是二次方程!')
    else:
        delta = b*b-4*a*c
        x = -b/(2*a)
        if delta == 0:
            print('方程有惟一解，X=%f'%(x))
            return x
        elif delta > 0:
            x1 = x-np.sqrt(delta)/(2*a)
            x2 = x+np.sqrt(delta)/(2*a)
            #print('方程有两个实根:X1=%f,X2=%f'%(x1,x2))
            return x2 #x2看起来是温度
        else:
            x1 = (-b+complex(0,1)*np.sqrt((-1)*delta))/(2*a)
            x2 = (-b-complex(0,1)*np.sqrt((-1)*delta))/(2*a)
            print('方程有两个虚根，如下所示：')
            print(x1,x2)
            return x1,x2

def calcVoltaverage(channel1,channel2):
    a=0
    for i in range (0,10):
        a=a+calcResistance(channel1,channel2)
        print("i==",i)
        print ("a=-",a)
        print("resistance average in 10 times is",a/10)
        print("-------------------------------------")  
        
        if i==9:
            a=0
            i=0
    
    return a/10


# led.on()
if __name__ == '__main__':
    flag=0
    while True:
        time.sleep(0.5)
        
        print("Pt1000で測温："+str(calcTemp((-0.0000005775),0.0039083,(1-calcVoltaverage(0,1)/1000))))
        flag=flag+1
        print("flag==",flag)
        # print("温度センサーで測温："+str(adt7410.read_adt7410()))
        print("-------------------------------------")
        pass
