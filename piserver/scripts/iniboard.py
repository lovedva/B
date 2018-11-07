#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import libraries
import pygame
from pygame.locals import *
import time
import os
import sys
import subprocess
import tty, termios
import RPi.GPIO


# 设置全局变量 setup global variables at first
# setup input pins,edit pin number here
InputA=16  #GPIO16 为A输入
InputB=7   #GPIO7 为B输入
InputC=8   #GPIO8 为C输入
InputD=15  #GPIO15 as inputD

# setup output pin for 电位器
reCS=13   #GPIO13 for UC
reINC=11  #GPIO11 for INC
reUD=22

# setup GPIO triggered  记录按钮输入状态（是否按下）
A_triggered= False
B_triggered= False
C_triggered= False
D_triggered= False

# 树莓派基本设定
# set up BCM GPIO numbering
RPi.GPIO.setmode(RPi.GPIO.BCM)

# set pins to input mode and pull up to high level(if necessary).
RPi.GPIO.setup(InputA, RPi.GPIO.IN,pull_up_down=RPi.GPIO.PUD_DOWN)
RPi.GPIO.setup(InputB, RPi.GPIO.IN,pull_up_down=RPi.GPIO.PUD_DOWN)
RPi.GPIO.setup(InputC, RPi.GPIO.IN,pull_up_down=RPi.GPIO.PUD_DOWN)
RPi.GPIO.setup(InputD, RPi.GPIO.IN,pull_up_down=RPi.GPIO.PUD_DOWN)

# set pins for LEDs to output mode
RPi.GPIO.setup(reCS, RPi.GPIO.OUT)
RPi.GPIO.setup(reINC, RPi.GPIO.OUT)
RPi.GPIO.setup(reUD, RPi.GPIO.OUT)
#RPi.GPIO.setup(LED3, RPi.GPIO.OUT)

# Define serveral threaded callback functions to run in another thread when events are detected
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

# define a function to turn on 电位器针脚
def turnon(re_PIN):
    RPi.GPIO.output(re_PIN, True)
    print ("| %sの出力 ==%s |"%((getPIN_NAME(re_PIN),RPi.GPIO.input(re_PIN))))
    print ("-------------------------------")

def getPIN_NAME(re_PIN):
    global reCS
    global reINC
    global reUD

    if re_PIN==reCS:
        return "CS"
    if re_PIN==reINC:
        return "INC"
    if re_PIN==reUD:
        return "UD"


def turnoff(re_PIN):
    RPi.GPIO.output(re_PIN, False)
    print ("| %sの出力 ==%s |"%((getPIN_NAME(re_PIN),RPi.GPIO.input(re_PIN))))
    print ("-------------------------------")




def init():
    print ("板子初始化完毕")
    RPi.GPIO.output(reCS, True)
    print ("| %sの出力 ==%s |"%((getPIN_NAME(reCS),RPi.GPIO.input(reCS))))
    RPi.GPIO.output(reINC, False)
    print ("| %sの出力 ==%s |"%((getPIN_NAME(reINC),RPi.GPIO.input(reINC))))
    RPi.GPIO.output(reUD, False)
    print ("| %sの出力 ==%s |"%((getPIN_NAME(reUD),RPi.GPIO.input(reUD))))

	
# detect rising edge
# when a rising edge is detected on pin,the callback functions will be run
RPi.GPIO.add_event_detect(InputA, RPi.GPIO.RISING,callback=SwitchA,bouncetime=200 ) # when use real Input swtich to switch the input level,
RPi.GPIO.add_event_detect(InputB, RPi.GPIO.RISING,callback=SwitchB,bouncetime=200 ) # bouncetime=[time] to debounce the switch.
RPi.GPIO.add_event_detect(InputC, RPi.GPIO.RISING,callback=SwitchC,bouncetime=200 )
RPi.GPIO.add_event_detect(InputD, RPi.GPIO.RISING,callback=SwitchD,bouncetime=200 )


try:
#初始化电位器  CS=H INC=L UD=L
    init()

finally:
    RPi.GPIO.cleanup() 




