#!/usr/bin/env python
# -*- coding: utf-8 -*-
#pt1000温度测定，数模转换mcp3008
# import max31855
import time
import numpy as np
import ads1248
import RPi.GPIO
# from gpiozero import PWMLED

Vref=3.3100 #V
I01=0.001000 #90 
I23=0.001000 #70  
I45=0.001000 #60  

def calcResistance(chls):

    if chls==01: #90
        #print("Pt1000's resistance now is: ",(voltage1-voltage0)/I01)
        # print("I01==",I01)
        return ((ads1248.readAdcChannel(01))/I01) #单位欧姆
    elif chls==23: #70
        #print("Pt1000's resistance now is: ",(voltage1-voltage0)/I23)
        # print("I23==",I23)
        return ((ads1248.readAdcChannel(23))/I23)
    elif chls==45: #50
        # print("Pt1000's resistance now is: ",((voltage1-voltage0)/I45))
        # print("I45==",I45)
        return ((ads1248.readAdcChannel(45))/I45)
    else:
        print("请输入正确的通道")

    # print("Pt1000's resistance now is: ",(voltage1-voltage0)/I)

    # return (voltage1-voltage0)/I #单位欧姆

def solveEquation(a,b,c):
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

def calcTemp(chls):
    return float(solveEquation((-0.0000005775),0.0039083,(1-calcResistance(chls)/1000))-0.1)


# led.on()
if __name__ == '__main__':
    flag=0
    try:
        ads1248.init()
        RPi.GPIO.output(3,RPi.GPIO.HIGH)
        while True:
            time.sleep(0.5)
            try:
                print("温度センサーで測温[热电偶]："+str(max31855.sensor.readTempC()))
            except:
                pass
            print("Pt1000で測温      [ch0,ch1]："+str(calcTemp(01)))
            print("Pt1000で測温      [ch2,ch3]："+str(calcTemp(23)))
            print("Pt1000で測温      [ch4,ch5]："+str(calcTemp(45)))
            
            flag=flag+1
            print("flag==",flag)
            

    finally:
        RPi.GPIO.output(3,RPi.GPIO.LOW)
        RPi.GPIO.cleanup()
        print("程序结束")
     