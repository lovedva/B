#!/usr/bin/env python
# -*- coding: utf-8 -*-

#旋转编码器

import time
import datetime
import RPi.GPIO
from gpiozero import PWMLED

#接受编码器针脚编号设置
encoderOUTA=20
encoderOUTB=21
encoderOUTZ=26

# LED0 指示灯 
LED0=6
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

#设置反馈方法
def Arise(channel):   #按钮A反馈方法线程
    global A_triggered
    A_triggered= True
    print("Afall")

def Afall(channel):   #按钮B反馈方法线程
    global A_triggered
    A_triggered= False
    print("Afall")

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
RPi.GPIO.add_event_detect(encoderOUTA, RPi.GPIO.RISING,callback=Arise,bouncetime=200 ) # when use real Input swtich to switch the input level,
RPi.GPIO.add_event_detect(encoderOUTB, RPi.GPIO.FALLING,callback=Afall,bouncetime=200 )
RPi.GPIO.add_event_detect(encoderOUTB, RPi.GPIO.RISING,callback=SwitchB,bouncetime=200 ) # bouncetime=[time] to debounce the switch.
RPi.GPIO.add_event_detect(encoderOUTZ, RPi.GPIO.RISING,callback=SwitchZ,bouncetime=200 )

if __name__ == "__main__":
    print("main start")
    led0.value=0
    print("LED0の出力GPIOは：６")
    print("Encoder Aの入力GPIOは：20")
    print("Encoder Bの入力GPIOは：21")
    print("Encoder Zの入力GPIOは：26")
    print("入力を待っている。。")
    try:
# 主循环
        while True:
            time.sleep(0.05)
 #第一次输入为A            
            if A_triggered and B_triggered==False:
                print("1番目の入力：A==Rising,B==0,2番目の入力を待っている。。。")
                TriggeredAllFalse()
    #第二次输入为B
                while True:
                        time.sleep(0.05)
                        if B_triggered:
                            if led0.value<=0.9:
                                led0.value+=0.1
                            elif led0.value==1:
                                RPi.GPIO.output(LED0, True)
                            print("2番目の入力：B==RIising,終わり。1番目の入力を待っている。。。")
                            B_triggered=False
                            A_triggered=False
                            break
  #第一次输入为B                      
            if B_triggered and A_triggered==False:
                TriggeredAllFalse()
                print("1番目の入力：B==Rising,A==0,2番目の入力を待っている。。。")       
    #第二次输入为A
                while True:
                    time.sleep(0.05)
                    if A_triggered:
                        if led0.value>=0.1:
                            led0.value-=0.1
                        elif led0.value==0:
                            RPi.GPIO.output(LED0, False)
                        print("2番目の入力：A==RIising,終わり。1番目の入力を待っている。。。")
                        B_triggered=False
                        A_triggered=False
                        break    

    finally:
        RPi.GPIO.cleanup()
