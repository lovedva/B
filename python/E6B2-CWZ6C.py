#!/usr/bin/env python
# -*- coding: utf-8 -*-

#旋转编码器

import pygame
import time
import os
import sys
import RPi.GPIO

#接受编码器针脚编号设置
encoderOUTA=20
encoderOUTB=21
encoderOUTZ=26

# LED0 指示灯 
LED0=6 # 

#设置针脚编号方式
RPi.GPIO.setmode(RPi.GPIO.BCM)

#设置输入针脚
RPi.GPIO.setup(encoderOUTA, RPi.GPIO.IN,pull_up_down=RPi.GPIO.PUD_DOWN)
RPi.GPIO.setup(encoderOUTB, RPi.GPIO.IN,pull_up_down=RPi.GPIO.PUD_DOWN)
RPi.GPIO.setup(encoderOUTZ, RPi.GPIO.IN,pull_up_down=RPi.GPIO.PUD_DOWN)

#设置事件检测
# when a rising edge is detected on pin,the callback functions will be run
RPi.GPIO.add_event_detect(encoderOUTA, RPi.GPIO.RISING,callback=SwitchA,bouncetime=200 ) # when use real Input swtich to switch the input level,
RPi.GPIO.add_event_detect(encoderOUTB, RPi.GPIO.RISING,callback=SwitchB,bouncetime=200 ) # bouncetime=[time] to debounce the switch.
RPi.GPIO.add_event_detect(encoderOUTZ, RPi.GPIO.RISING,callback=SwitchC,bouncetime=200 )
