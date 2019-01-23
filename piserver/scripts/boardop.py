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
import smbus


# 设置全局变量 setup global variables at first
# setup input pins,edit pin number here
InputA=16  #GPIO16 为A输入
InputB=7   #GPIO7 为B输入
InputC=8   #GPIO8 为C输入
InputD=15  #GPIO15 as inputD

# setup output pins
LED0=4  #GPIO for UC
In1_Motor=13   #GPIOXX 
In2_Motor=19

# setup GPIO triggered  记录按钮输入状态（是否按下）
A_triggered= False
B_triggered= False
C_triggered= False
D_triggered= False

def init():
# 树莓派基本设定
# set up BCM GPIO numbering
    RPi.GPIO.setmode(RPi.GPIO.BCM)

    # set pins to input mode and pull up to high level(if necessary).
    RPi.GPIO.setup(InputA, RPi.GPIO.IN,pull_up_down=RPi.GPIO.PUD_DOWN)
    RPi.GPIO.setup(InputB, RPi.GPIO.IN,pull_up_down=RPi.GPIO.PUD_DOWN)
    RPi.GPIO.setup(InputC, RPi.GPIO.IN,pull_up_down=RPi.GPIO.PUD_DOWN)
    RPi.GPIO.setup(InputD, RPi.GPIO.IN,pull_up_down=RPi.GPIO.PUD_DOWN)

    # set pins for LEDs to output mode
    RPi.GPIO.setup(LED0, RPi.GPIO.OUT)
    RPi.GPIO.setup(In1_Motor, RPi.GPIO.OUT)
    RPi.GPIO.setup(In2_Motor, RPi.GPIO.OUT)
#RPi.GPIO.setup(LED3, RPi.GPIO.OUT)

init()

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

def getPIN_NAME(PIN):
    global LED0
    if PIN==LED0:
        return "LED0"
        
def getPIN_NUM(strPINNAME):
    global LED0
    if strPINNAME=="LED0":
        return LED0
    # if strPINNAME=="In1_Motor":
    #     return LED0
    # if strPINNAME=="LED0":
    #     return LED0

# define a function to pull up pin
def turnon(PIN):
    RPi.GPIO.output(PIN, True)
    print ("| %sの出力 ==%s |"%((getPIN_NAME(PIN),RPi.GPIO.input(PIN))))
    print ("-------------------------------")

def turnoff(PIN):
    RPi.GPIO.output(PIN, False)
    print ("| %sの出力 ==%s |"%((getPIN_NAME(PIN),RPi.GPIO.input(PIN))))
    print ("-------------------------------")
	
# detect rising edge
# when a rising edge is detected on pin,the callback functions will be run
RPi.GPIO.add_event_detect(InputA, RPi.GPIO.RISING,callback=SwitchA,bouncetime=200 ) # when use real Input swtich to switch the input level,
RPi.GPIO.add_event_detect(InputB, RPi.GPIO.RISING,callback=SwitchB,bouncetime=200 ) # bouncetime=[time] to debounce the switch.
RPi.GPIO.add_event_detect(InputC, RPi.GPIO.RISING,callback=SwitchC,bouncetime=200 )
RPi.GPIO.add_event_detect(InputD, RPi.GPIO.RISING,callback=SwitchD,bouncetime=200 )

#adt7410 i2c操作
# def read_adt7410():
#     word_data = bus.read_word_data(address_adt7410, register_adt7410)
#     data = (word_data & 0xff00)>>8 | (word_data & 0xff)<<8
#     data = data>>3 # 13ビットデータ
#     if data & 0x1000 == 0:  # 温度が正または0の場合
#         temperature = data*0.0625
#     else: # 温度が負の場合、 絶対値を取ってからマイナスをかける
#         temperature = ( (~data&0x1fff) + 1)*-0.0625
#     return temperature

# bus = smbus.SMBus(1)
# address_adt7410 = 0x48
# register_adt7410 = 0x00
#
#---adt7410 i2c操作结束

#板子操作方法
# try:

turnon(LED0)
print ("板子初始化完毕，LED0==ON")
print("导入boradop.py")

# finally:
#     RPi.GPIO.cleanup() 
