#!/usr/bin/env python
# -*- coding: utf-8 -*-

#旋转编码器

import time
import datetime
import RPi.GPIO
from gpiozero import PWMLED

#接受编码器针脚编号设置
encoderOUTA=27
encoderOUTB=17
encoderOUTZ=26

# LED0 指示灯 
LED0=10
led0=PWMLED(LED0) 

# setup GPIO triggered  记录按钮输入状态（是否按下）
A_triggered= False
B_triggered= False
Z_triggered= False

#设置针脚编号方式
RPi.GPIO.setmode(RPi.GPIO.BCM)

#设置输入针脚
RPi.GPIO.setup(encoderOUTA, RPi.GPIO.IN,pull_up_down=RPi.GPIO.PUD_DOWN)
RPi.GPIO.setup(encoderOUTB, RPi.GPIO.IN,pull_up_down=RPi.GPIO.PUD_DOWN)
RPi.GPIO.setup(encoderOUTZ, RPi.GPIO.IN,pull_up_down=RPi.GPIO.PUD_DOWN)

#设置输出针脚
RPi.GPIO.setup(LED0,RPi.GPIO.OUT)

#设置反馈方法
def SwitchA(channel):   
    global A_triggered
    if RPi.GPIO.input(encoderOUTA):
        A_triggered= True
        print("A == rise, A_triggered==True")
    else:
        A_triggered=False
        print("A == fall, A_triggered==False")

def SwitchB(channel):   
    global B_triggered
    if RPi.GPIO.input(encoderOUTB):
        B_triggered= True
        print("B == rise,B_triggered==True")
    else:
        B_triggered=False
        print("B == fall,B_triggered==False")

def SwitchZ(channel):
    global Z_triggered
    Z_triggered= True

def TriggeredAllFalse():  #将所有开关输入状态设置为否
    global A_triggered
    global B_triggered
    global Z_triggered
    A_triggered= False
    B_triggered= False
    Z_triggered= False

#设置事件检测
# when a rising edge is detected on pin,the callback functions will be run
RPi.GPIO.add_event_detect(encoderOUTA, RPi.GPIO.BOTH,callback=SwitchA,bouncetime=5 ) # when use real Input swtich to switch the input level,
RPi.GPIO.add_event_detect(encoderOUTB, RPi.GPIO.BOTH,callback=SwitchB,bouncetime=5 ) # when use real Input swtich to switch the input level,
RPi.GPIO.add_event_detect(encoderOUTZ, RPi.GPIO.RISING,callback=SwitchZ,bouncetime=5 )

#设定循环等待时间
TIME=0.001


if __name__ == "__main__":
    print("main start")
    led0.value=0
    print("LED0の出力GPIOは：10，順番で入力するとLED0の明るさを変えることができます")	
    print("Encoder Aの入力GPIOは：27")
    print("Encoder Bの入力GPIOは：17")
    print("Encoder Zの入力GPIOは：26")
    print("入力を待っている。。")
    try:
# 主循环
        while True:
            time.sleep(TIME)
 #第一次输入为A升高            
            if A_triggered and B_triggered==False:
                print("1番目の入力：A==Rising,B==0,2番目の入力を待っている。。。")
                # TriggeredAllFalse()
    #第二次输入为B升高
                while True:
                    time.sleep(TIME)
                    if B_triggered:
                        print("入力2==B rise，入力3を待っている。。。")
        #第三次输入为A下降
                        while True:
                            time.sleep(TIME)
                            if A_triggered==False:
                                print("入力3==A fall，入力4を待っている。。。")
            #第四次输入为B下降
                                while True:
                                    time.sleep(TIME)
                                    if B_triggered==False:
                                        print("入力4==B fall。回転方向： CW ")
                                        if led0.value<=0.99:
                                            led0.value+=0.01
                                        elif led0.value==1:
                                            RPi.GPIO.output(LED0, True)
                                        break #退出第四次循环
                                break  #退出第三次循环
        #第三次输入为B下降                                
                            elif B_triggered==False:
                                print("入力3==B fall")
                                break #退出第三次循环
                        print("入力1に戻る，入力1を待っている。。。")
                        break #退出第二层循环           
    #第二次输入为A下降
                    elif A_triggered==False:
                        print("入力1に戻る，入力1を待っている。。。")
                        break #退出第二次循环


  #第一次输入为B升高                      
            if B_triggered and A_triggered==False:
                print("1番目の入力：B==Rising,A==0,2番目の入力を待っている。。。")       
    #第二次输入为A升高            
                while True:
                    time.sleep(TIME)
                    if A_triggered:
                        print("入力2==A rise，入力3を待っている。。。")
        #第三次输入为B下降
                        while True:
                            time.sleep(TIME)
                            if B_triggered==False:
                                print("入力3==B fall，入力4を待っている。。。")
            #第四次输入为A下降
                                while True:
                                    time.sleep(TIME)
                                    if A_triggered==False:
                                        print("入力4==A fall。回転方向： CWW ")
                                        if led0.value>=0.01:
                                               led0.value-=0.01
                                        elif led0.value==0:
                                            RPi.GPIO.output(LED0, False)
                                        break #退出第四次循环
                                break  #退出第三次循环
        #第三次输入为A下降                                
                            elif A_triggered==False:
                                print("入力3==A fall")
                                break #退出第三次循环
                        print("入力1に戻る，入力1を待っている。。。")
                        break #退出第二层循环           
    #第二次输入为B下降
                    elif B_triggered==False:
                        print("入力2==B fall")
                        print("入力1に戻る，入力1を待っている。。。")
                        break #退出第二次循环

                        
    finally:
        RPi.GPIO.cleanup()
