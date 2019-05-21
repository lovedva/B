#!/usr/bin/env python
# -*- coding: utf-8 -*-
#pt1000温度测定，数模转换mcp3008
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import time
import numpy as np
import adt7410
import RPi.GPIO
# from gpiozero import PWMLED

Vref=3.3100 #V
I01=0.000996 #90 #0.5125mA
I23=0.0010 #70  #0.513
I45=0.0010 #60          #0.535

Vref=3.31 #V


# led = PWMLED(12)  #供电端口 gpio12
CLK  = 26   #mcp3008接ch0ch4
MISO = 20     #Dout
MOSI = 10     #Din
CS   = 27     #slect
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

def calcResistance(channel1,channel2):


    adc0 = mcp.read_adc(channel1)
    adc1=mcp.read_adc(channel2)
    voltage0 = Vref * (adc0/1023.00)
    voltage1 = Vref * (adc1/1023.00)
    
    # print("channel 0 voltage is ",voltage0)
    # print("channel 1 voltage is ",voltage1)

    #print("V1-V0 is",(voltage1-voltage0))

    if channel1==0: #90
        #print("Pt1000's resistance now is: ",(voltage1-voltage0)/I01)
        # print("I01==",I01)
        return ((voltage1-voltage0)/I01) #单位欧姆
    elif channel1==2: #70
        #print("Pt1000's resistance now is: ",(voltage1-voltage0)/I23)
        # print("I23==",I23)
        return ((voltage1-voltage0)/I23)
    elif channel1==4: #50
        # print("Pt1000's resistance now is: ",((voltage1-voltage0)/I45))
        # print("I45==",I45)
        return ((voltage1-voltage0)/I45)

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

def calcTemp(ch1,ch2):
    return float(solveEquation((-0.0000005775),0.0039083,(1-calcVoltaverage(ch1,ch2)/1000))-0.1)

def calcVoltaverage(channel1,channel2):
    a=0
    b=0
    list = []
    # for j in range(0,5):
    for i in range (0,10):
        time.sleep(0.02)
        a=a+calcResistance(channel1,channel2)
        # print("i==",i)
        # print ("a=-",a)
        # print("resistance average in 10 times is",a/20)
        # print("-------------------------------------")  
        
        if i==9:
            b=a/10
            a=0
            i=0
            list.append(b)
            # print "a/10==",b

        # if j==4:
        #     # print "max list==",max(list),"index==",list.index(max(list))
        #     # print "min list==",min(list),"index==",list.index(min(list))
        #     sum=list[0]+list[1]+list[2]+list[3]+list[4]#+list[5]+list[6]+list[7]+list[8]+list[9]
        #     # print "total list==",sum
        #     sum2=sum-list[list.index(max(list))]-list[list.index(max(list))]
        #     # print "get rid of max and min",sum2
        #     c=sum2/3
        #     print"resistance average final==",c
    return b


# led.on()
if __name__ == '__main__':
    flag=0
    try:
        while True:
            time.sleep(0.4)
            try:
                print("温度センサーで測温[ch0,ch1]："+str(adt7410.read_adt7410()))
            except:
                pass
            print("Pt1000で測温      [ch0,ch1]："+str(calcTemp(0,1)))
            print("Pt1000で測温      [ch2,ch3]："+str(calcTemp(2,3)))
            print("Pt1000で測温      [ch4,ch5]："+str(calcTemp(4,5)))
            
            flag=flag+1
            print("flag==",flag)
            # print("温度センサーで測温："+str(adt7410.read_adt7410()))        print("-------------------------------------")

    finally:
        RPi.GPIO.cleanup()
        print("程序结束")
     