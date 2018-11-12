#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import time
import os
import sys
import subprocess
import tty, termios
import RPi.GPIO

# setup input pin for motor
In1_Motor=13   #GPIOXX 
In2_Motor=19  #GPIOXX 

# LED1 指示灯 pin
outPutLED=6 # GPIO6 此灯亮表示程序启动完毕

# setup input pins,edit pin number here
InputA=16  #GPIO16 为手柄B输入 键盘【A】 正转    
InputB=7   #GPIO7 为X输入 键盘【D】 反转
InputC=8   #GPIO8 为Start输入 键盘【B】 重启（重新连接蓝牙）
InputD=15  #GPIO15 as inputY 键盘【S】 停止

# set up BCM GPIO numbering
RPi.GPIO.setmode(RPi.GPIO.BCM)

# set Motor Diver's Input Pin to output mode
RPi.GPIO.setup(In1_Motor, RPi.GPIO.OUT)
RPi.GPIO.setup(In2_Motor, RPi.GPIO.OUT)
RPi.GPIO.setup(outPutLED, RPi.GPIO.OUT)

## output GPIOs Initial
RPi.GPIO.output(In1_Motor, False)
RPi.GPIO.output(In2_Motor, False)
RPi.GPIO.output(outPutLED, False)

# setup GPIO triggered  记录按钮输入状态（是否按下）
A_triggered= False
B_triggered= False
C_triggered= False
D_triggered= False

# set pins to input mode and pull up to high level(if necessary).
RPi.GPIO.setup(InputA, RPi.GPIO.IN,pull_up_down=RPi.GPIO.PUD_DOWN)
RPi.GPIO.setup(InputB, RPi.GPIO.IN,pull_up_down=RPi.GPIO.PUD_DOWN)
RPi.GPIO.setup(InputC, RPi.GPIO.IN,pull_up_down=RPi.GPIO.PUD_DOWN)
RPi.GPIO.setup(InputD, RPi.GPIO.IN,pull_up_down=RPi.GPIO.PUD_DOWN)

#设置反馈方法
def SwitchA(channel):   #按钮A反馈方法线程
    #if RPi.GPIO.input(InputA):
            global A_triggered
            A_triggered= True

def SwitchB(channel):   #按钮B反馈方法线程
    #if RPi.GPIO.input(InputB):
            global B_triggered
            B_triggered= True

def SwitchC(channel):
    #if RPi.GPIO.input(InputC):
        global C_triggered
        C_triggered= True

def SwitchD(channel):
    #if RPi.GPIO.input(InputD):
        global D_triggered
        D_triggered= True

def TriggeredAllFalse():  #将所有开关输入状态设置为否
    global A_triggered
    global B_triggered
    global C_triggered
    global D_triggered
    A_triggered= False
    B_triggered= False
    C_triggered= False
    D_triggered= False

 #设置事件检测
 # when a rising edge is detected on pin,the callback functions will be run
RPi.GPIO.add_event_detect(InputA, RPi.GPIO.RISING,callback=SwitchA,bouncetime=200 ) # when use real Input swtich to switch the input level,
RPi.GPIO.add_event_detect(InputB, RPi.GPIO.RISING,callback=SwitchB,bouncetime=200 ) # bouncetime=[time] to debounce the switch.
RPi.GPIO.add_event_detect(InputC, RPi.GPIO.RISING,callback=SwitchC,bouncetime=200 )
RPi.GPIO.add_event_detect(InputD, RPi.GPIO.RISING,callback=SwitchD,bouncetime=200 )


#定义重启方法，蓝牙断线后使用
def restart_program():
    print "启动重启，0.2秒后重启本程序。。。"
    RPi.GPIO.output(outPutLED, False)
    time.sleep(0.05)
    RPi.GPIO.output(outPutLED, True)
    time.sleep(0.05)
    RPi.GPIO.output(outPutLED, False)
    time.sleep(0.05)
    RPi.GPIO.output(outPutLED, True)
    time.sleep(0.05)
    RPi.GPIO.output(outPutLED, False)
    python = sys.executable
    os.execl(python, python, * sys.argv)

#初始化Joystick
pygame.joystick.init()


try:
    #创建Joystick对象并初始化
    joystick0 = pygame.joystick.Joystick(0) 
    joystick0.init()

    #打印手柄参数
    print("Joystick数量：")
    print(pygame.joystick.get_count())
    print("Joystick ID：")
    print(joystick0.get_id())
    print("Joystick名称：")
    print(joystick0.get_name())
except Exception as e:
    print "没有连接蓝牙手柄，如果需要连接蓝牙设备，请开启蓝牙设备后按SW1按键重启本程序"
    RPi.GPIO.output(outPutLED, False)
    time.sleep(0.2)
    RPi.GPIO.output(outPutLED, True)
    time.sleep(0.2)
    RPi.GPIO.output(outPutLED, False)
    time.sleep(0.2)
    RPi.GPIO.output(outPutLED, True)
    time.sleep(0.2)
    RPi.GPIO.output(outPutLED, False)
    time.sleep(0.2)
    RPi.GPIO.output(outPutLED, True)
    time.sleep(0.2)
    RPi.GPIO.output(outPutLED, False)
    time.sleep(0.2)
    # RPi.GPIO.output(outPutLED, True)
    # time.sleep(0.1)
    # RPi.GPIO.output(outPutLED, False)
    # time.sleep(0.1)
    # RPi.GPIO.output(outPutLED, True)
    # time.sleep(0.1)
    # RPi.GPIO.output(outPutLED, False)
    pass

#pygame初始化
pygame.init()

#主循环
try:
    flag=0
    RPi.GPIO.output(outPutLED, True)
    print "程序启动完毕"
    print "正在读取输入，请使用蓝牙手柄或者接线按钮输入"
    #主循环开始
    while True:
        time.sleep(0.1)
        # 获取事件
        eventlist = pygame.event.get()
        # 手柄事件（pygame）
        for e in eventlist:
            if e.type == QUIT:
                break
            # if e.type ==pygame.KEYDOWN:
            #     if event.key == pygame.K_b:
            #         restart_program()
            elif e.type == pygame.locals.JOYAXISMOTION:
                x, y = joystick0.get_axis(0), joystick0.get_axis(1)
                print 'axis x:' + str(x) + ' axis y:' + str(y)
            elif e.type == pygame.locals.JOYHATMOTION:
                x, y = joystick0.get_hat(0)
                print 'hat x:' + str(x) + ' hat y:' + str(y)
            elif e.type == pygame.locals.JOYBUTTONDOWN:
                print 'button:' + str(e.button)
                if e.button==2: #B
                    print 'Button B pressed' 
                    SwitchA(1)
                elif e.button==1: #X
                    print 'Button X pressed' 
                    SwitchB(1)
                elif e.button==0 or e.button==3: #A or Y
                    print 'Button A pressed' 
                    SwitchD(1)
                # elif e.button==3: #Y
                #     print 'Button Y pressed' 
                #     global D_triggered
                #     D_triggered= True

                    
        # 开关控制事件 （trigger事件）
        if A_triggered: #正转
            time.sleep(0.3)  #此处等待为防止同时按下多个按钮  
            print '----------------'
            print '【move forward】'
            print '----------------'
            RPi.GPIO.output(In1_Motor, True)
            RPi.GPIO.output(In2_Motor, False)
            print "In1_Motor 输出为："
            print (RPi.GPIO.input(In1_Motor))
            print "In2_Motor 输出为："
            print (RPi.GPIO.input(In2_Motor))
            A_triggered=False #把按钮A设为关闭
            

        elif B_triggered: #反转
            time.sleep(0.3)
            print '----------------'
            print "【move backward】"
            print '----------------'
            RPi.GPIO.output(In1_Motor, False)
            RPi.GPIO.output(In2_Motor, True)
            B_triggered=False
            

        elif C_triggered: #【R】重启程序
            print '----------------'
            print '【bluetooth reconnect ...】'
            print '----------------'
            restart_program()
            C_triggered=False
            time.sleep(0.2)

        elif D_triggered: #【S】停止
            print '----------------'
            print '【Stop】'
            print '----------------'
            RPi.GPIO.output(In1_Motor, False)
            RPi.GPIO.output(In2_Motor, False)
            D_triggered=False
            time.sleep(0.1)

    print "Reading from gamepad or buttons:"

finally:
    RPi.GPIO.cleanup() 
