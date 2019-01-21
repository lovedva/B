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

# setup output pin for 电位器
CS=13   #GPIO13 for UC
INC=11  #GPIO11 for INC
UD=22


# setup GPIO triggered  记录按钮输入状态（是否按下）
A_triggered= False
B_triggered= False
C_triggered= False
D_triggered= False

# 树莓派基本设定
# set up BCM GPIO numbering
RPi.GPIO.setmode(RPi.GPIO.BCM)

# set pins to input mode and pull up to high level(if necessary).

# set pins for LEDs to output mode
RPi.GPIO.setup(CS, RPi.GPIO.OUT)
RPi.GPIO.setup(INC, RPi.GPIO.OUT)
RPi.GPIO.setup(UD, RPi.GPIO.OUT)
#RPi.GPIO.setup(LED3, RPi.GPIO.OUT)


# define a function to turn on 电位器针脚
def turnon(re_PIN):
    RPi.GPIO.output(re_PIN, True)
    print ("| %sの出力 ==%s |"%((getPIN_NAME(re_PIN),RPi.GPIO.input(re_PIN))))
    print ("-------------------------------")

def getPIN_NAME(re_PIN):
    global CS
    global INC
    global UD

    if re_PIN==CS:
        return "CS"
    if re_PIN==INC:
        return "INC"
    if re_PIN==UD:
        return "UD"


def turnoff(re_PIN):
    RPi.GPIO.output(re_PIN, False)
    print ("| %sの出力 ==%s |"%((getPIN_NAME(re_PIN),RPi.GPIO.input(re_PIN))))
    print ("-------------------------------")




def init():
		
    RPi.GPIO.output(CS, True)
    print ("| %sの出力 ==%s |"%((getPIN_NAME(CS),RPi.GPIO.input(CS))))
    RPi.GPIO.output(INC, False)
    print ("| %sの出力 ==%s |"%((getPIN_NAME(INC),RPi.GPIO.input(INC))))
    RPi.GPIO.output(UD, False)
    print ("| %sの出力 ==%s |"%((getPIN_NAME(UD),RPi.GPIO.input(UD))))

	
# detect rising edge
# when a rising edge is detected on pin,the callback functions will be run
RPi.GPIO.add_event_detect(InputA, RPi.GPIO.RISING,callback=SwitchA,bouncetime=200 ) # when use real Input swtich to switch the input level,
RPi.GPIO.add_event_detect(InputB, RPi.GPIO.RISING,callback=SwitchB,bouncetime=200 ) # bouncetime=[time] to debounce the switch.
RPi.GPIO.add_event_detect(InputC, RPi.GPIO.RISING,callback=SwitchC,bouncetime=200 )
RPi.GPIO.add_event_detect(InputD, RPi.GPIO.RISING,callback=SwitchD,bouncetime=200 )



if __name__ == '__main__':
    main()

def main():    
    try:

        start = time.time()
        print ("テストプログラム開始。。。")
        print ("------------------------------")
        print ("#GPIO13 CS入力")
        print ("#GPIO11 INC入力")
        print ("#GPIO9 　UD入力")
        time.sleep(0.5)
        print ("------------------------------")
        print "A=正方向 S=停止 D=逆方向　Q=Quit"

    #初始化电位器  CS=H INC=L UD=L
        init()

    	#主循环开始
        while  True:
    	#get events of the controller
            fd=sys.stdin.fileno()
            old_settings=termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch=sys.stdin.read(1)
          	finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)  
                #print 'error'
            if ch=='a':
                turnoff(CS)
                turnon(UD)
                turnon(INC)
                time.sleep(0.05)
                turnoff(INC)
                print '----------------'
                print '【 Slide <<<< 】'
                print '----------------'
                time.sleep(1) #此处等待为防止同时按下多个按钮
            # elif ch=='w':
            #     print '----------------'
            #     print '【Break】'
            #     print '----------------'
            #     RPi.GPIO.output(In1_Motor, True)
            #     RPi.GPIO.output(In2_Motor, True)
            #     time.sleep(0.2)
            elif ch=='s':
                init()
                print '----------------'
                print '【 Stop 】'
                print '----------------'
                time.sleep(0.2)
            elif ch=='d':
                turnoff(CS)
                turnoff(UD)
                turnon(INC)
                time.sleep(0.05)
                turnoff(INC)
                print '----------------'
                print "【 Slide >>>> 】"
                print '----------------'
                time.sleep(1)
            elif ch=='q':
                print '----------------'
                print "【 shutdown! 】"
                print '----------------'
                break
            elif ord(ch)==0x3: #这个是ctrl c
                
                print "shutdown"
                break
            print "Reading form keybord:"
            print "A=正方向 S=停止 D=逆方向　Q=Quit"

        print "Reading from keybord"

    finally:
        RPi.GPIO.cleanup() 




