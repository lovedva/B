#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------------------#
# PROJECT   :  RasPi Python :: Switch Input Sequences Test
# FILENAME  :  Switch_Input_Sequences.py
# Author    :  https://github.com/syjsxxjy
#
# Codes after "#" will not be run.
# This code shows how to input in sequences and determine if they are in the right sequences.
# This program will turn on LED0 when the 1st input is A and the 2nd input is B.Turn off
# LED0 if the input is BA.
# Here is the input sequences and output results:
# Input Sequences   Output Result
#   AB               LED0==True
#   A*(not B)        do nothing
#   BA               LED0==False
#   B*(not A)        do nothing
#   CD once          LED1==True
#   CD twice         LED2==True
#   CD 3 times       LED3==True
#   C 4 times        LED123==False
#   C*(not D)        LED123==False
#   D                LED123==False
#
# You can find this code here:
# https://github.com/syjsxxjy/WorkSpace/tree/master/python
# and download here:
# https://github.com/syjsxxjy/WorkSpace/releases
#
# References(参考文献):
# https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
#-----------------------------------------------------------------------------------------#

# import libraries
import RPi.GPIO
import time

# 设置全局变量 setup global variables at first
# setup input pins,edit pin number here
InputA=20  #GPIO16 为A输入
InputB=21   #GPIO7 为B输入
InputC=8   #GPIO8 为C输入
InputD=15  #GPIO15 as inputD

# setup output pin for LED
LED=13   #GPIO13 for LED
LED1=11  #GPIO11 for LED1
LED2=9
LED3=10

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
RPi.GPIO.setup(LED, RPi.GPIO.OUT)
RPi.GPIO.setup(LED1, RPi.GPIO.OUT)
RPi.GPIO.setup(LED2, RPi.GPIO.OUT)
RPi.GPIO.setup(LED3, RPi.GPIO.OUT)

# set up variables to save start and end time, initialize them to 0 as default
#TimeA=0.00
#TimeB=0.00

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

def TriggeredAllFalse():  #将所有输入状态设置为否
    global A_triggered
    global B_triggered
    global C_triggered
    global D_triggered
    A_triggered= False
    B_triggered= False
    C_triggered= False
    D_triggered= False

# define a function to turn on LED
def turnon(LED_Num):
        if LED_Num==LED1:
            led_Name=1
        elif LED_Num==LED2:
            led_Name=2
        elif LED_Num==LED3:
            led_Name=3
        elif LED_Num==LED:
            led_Name=0
        RPi.GPIO.output(LED_Num, True)
        print ("-------------------------------")   #【○ 】
        print ("| LED[%s]の出力 ==【○ 】(True) |"%(led_Name))
        print ("-------------------------------")

# define a function to turn off LED
def turnoff(LED_Num):
        if LED_Num==LED1:
            led_Name=1
        elif LED_Num==LED2:
            led_Name=2
        elif LED_Num==LED3:
            led_Name=3
        elif LED_Num==LED:
            led_Name=0
        RPi.GPIO.output(LED_Num, False)
        print ("---------------------------------")   #【× 】
        print ("| LED[%s]の出力 ==【× 】(False) |"%(led_Name))
        print ("---------------------------------")

def turnoff123():
    turnoff(LED1)
    turnoff(LED2)
    turnoff(LED3)

# detect rising edge
# when a rising edge is detected on pin,the callback functions will be run
RPi.GPIO.add_event_detect(InputA, RPi.GPIO.RISING,callback=SwitchA,bouncetime=200 ) # when use real button swtich to switch the input level,
RPi.GPIO.add_event_detect(InputB, RPi.GPIO.RISING,callback=SwitchB,bouncetime=200 ) # bouncetime=[time] to debounce the switch.
RPi.GPIO.add_event_detect(InputC, RPi.GPIO.RISING,callback=SwitchC,bouncetime=200 )
RPi.GPIO.add_event_detect(InputD, RPi.GPIO.RISING,callback=SwitchD,bouncetime=200 )

try:
    start = time.time()
    print ("AltとCを押すと,プログラムを中止する。")
    time.sleep(0.5)
    print ("ループ開始：１番目の入力を待つ... Wait for 1st input...")
    #print ("Press 'Alt+C' to quit ")

    ### main(1st) loop start,check for 1stInput
    while True:
        time.sleep(0.1)

        ### when 1stinput is B
        if B_triggered and A_triggered==False:
            if RPi.GPIO.input(LED3) or RPi.GPIO.input(LED2) or RPi.GPIO.input(LED1):
                TriggeredAllFalse()
                turnoff123()
                print("１番目の入力==[Button B],キー==[B],LED[1] or [2] or [3]はすでに点灯されている。LED123を消す。")
                print("最初に戻る。")
                #print ("1st input=[Button C],key==c,LED3 has been turned on already,turn off all the leds and back to the start")
                print ("１番目の入力を待つ...")
                #print ("loop start: Wait for 1st input...")
                continue
            else:
                TriggeredAllFalse()
                print("１番目の入力 == [Button B],２番目の入力を待つ...")

        ### 2nd loop,check for 2nd Input
            while True:
                time.sleep(0.1)
                if B_triggered and A_triggered==False:
                    print("２番目の入力==[Button B],キー==[BB](False),最初に戻る。")
                    time.sleep(0.5)
                    print ("１番目の入力を待つ...")
                    B_triggered=False
                    A_triggered=False
                    break

                elif A_triggered and B_triggered==False: ### when 2ndinput is A
                    B_triggered=False
                    A_triggered=False
                    turnoff(LED)
                    print("２番目の入力==[Button A],キー==[BA](True),LEDを消す。最初に戻る。")
                    time.sleep(0.3)
                    print ("１番目の入力を待つ...")
                    #print("2nd input=[Button A],encryption key==True,turnoff and back to the start")
                    #print ("loop start: Wait for 1st input...")
                    B_triggered=False
                    A_triggered=False
                    break

                elif A_triggered==True and B_triggered==True:
                    print("２番目の入力==[Error],キー==[Error],最初に戻る。")
                    time.sleep(0.3)
                    print ("１番目の入力を待つ...")
                    #print("2nd input==Wrong,back to start")
                    #print ("loop start: Wait for 1st input...")
                    B_triggered=False
                    A_triggered=False
                    break
                elif C_triggered:
                    print("２番目の入力==[Button C],キー==[BC](False),最初に戻る。")
                    time.sleep(0.3)
                    print ("１番目の入力を待つ...")
                    #print("2nd input=[Button C],Key==False,back to start")
                    #print ("Wait for 1st input...")
                    TriggeredAllFalse()
                    break
                elif D_triggered:
                    print("２番目の入力==[Button D],キー==[BD](False),最初に戻る。")
                    time.sleep(0.3)
                    print ("１番目の入力を待つ...")
                    #print("2nd input=[Button D],Key==False,back to start")
                    #print ("Wait for 1st input...")
                    TriggeredAllFalse()
                    break
                else:
                    continue

        ### when 1stinput is A
        elif A_triggered and B_triggered==False:
            TriggeredAllFalse()
            print("第一次输入：A==Rising,B==0,等待第二次输入。。")
                #print("1st input=[Button A],waiting for 2nd input...")

        ### 2nd loop,check for 2nd Input
            while True:
                time.sleep(0.1)
                if B_triggered and A_triggered==False:          ### when 2ndinput is B
                    B_triggered=False
                    A_triggered=False
                    turnon(LED)
                    print("２番目の入力==[Button B],キー==[AB](True),LEDをつける。最初に戻る。")
                    time.sleep(0.3)
                    print ("１番目の入力を待つ...")
                    #print("2nd input=[Button B],True,turnon the LED and back to start")
                    #print ("loop start: Wait for 1st input...")
                    break
                elif A_triggered and B_triggered==False:
                    print("２番目の入力==[Button A],キー==[AA](False),最初に戻る。")
                    time.sleep(0.3)
                    print ("１番目の入力を待つ...")
                    # print("2nd input=[Button A],False,back to start")
                    # print ("loop start: Wait for 1st input...")
                    B_triggered=False
                    A_triggered=False
                    break
                elif A_triggered==True and B_triggered==True:
                    print("２番目の入力==[Error],キー==[Error],最初に戻る。")
                    time.sleep(0.3)
                    print ("１番目の入力を待つ...")
                    # print("2nd input==Wrong,back to start")
                    # print ("loop start: Wait for 1st input...")
                    B_triggered=False
                    A_triggered=False
                    break
                elif C_triggered:
                    print("２番目の入力==[Button C],キー==[AC](False),最初に戻る。")
                    time.sleep(0.3)
                    print ("１番目の入力を待つ...")
                    # print("2nd input=[Button C],Key==False,back to start")
                    # print ("Wait for 1st input...")
                    TriggeredAllFalse()
                    break
                elif D_triggered:
                    print("２番目の入力==[Button D],キー==[AD](False),最初に戻る。")
                    time.sleep(0.3)
                    print ("１番目の入力を待つ...")
                    # print("2nd input=[Button D],Key==False,back to start")
                    # print ("Wait for 1st input...")
                    TriggeredAllFalse()
                    break
                else:
                    continue

        ### when 1stinput is C
        elif C_triggered and D_triggered==False:
            if RPi.GPIO.input(LED3):
                TriggeredAllFalse()
                turnoff123()
                print("１番目の入力==[Button C],キー==[C],LED3はすでに点灯されている。LED123を消す。")
                print("最初に戻る。")
                #print ("1st input=[Button C],key==c,LED3 has been turned on already,turn off all the leds and back to the start")
                print ("１番目の入力を待つ...")
                #print ("loop start: Wait for 1st input...")
                continue
            else:
                TriggeredAllFalse()
                print("１番目の入力 == [Button C],２番目の入力を待つ...")
                #print("1st input=[Button C],waiting for 2nd input...")


        ### 2nd loop,check for 2nd Input
            while True:
                time.sleep(0.1)
                if C_triggered and D_triggered==False:      ### when 2ndinput is C
                    TriggeredAllFalse()
                    turnoff123()
                    print("２番目の入力==[Button C],キー==[CC](False),LED123を消す。最初に戻る。")
                    time.sleep(0.3)
                    print ("１番目の入力を待つ...")
                    # print("2nd input=[Button C],False,turnoff all of the leds and back to start")
                    # print ("loop start: Wait for 1st input...")
                    break
                elif A_triggered and D_triggered==False:      ### when 2ndinput is A
                    TriggeredAllFalse()
                    turnoff123()
                    print("２番目の入力==[Button A],キー==[CA](False),LED123を消す。最初に戻る。")
                    time.sleep(0.3)
                    print ("１番目の入力を待つ...")
                    # print("2nd input=[Button A],False,turnoff all of the leds and back to start")
                    # print ("loop start: Wait for 1st input...")
                    break
                elif B_triggered and D_triggered==False:      ### when 2ndinput is B
                    TriggeredAllFalse()
                    turnoff123()
                    print("２番目の入力==[Button B],キー==[CB](False),LED123を消す。最初に戻る。")
                    time.sleep(0.3)
                    print ("１番目の入力を待つ...")
                    # print("2nd input=[Button B],False,turnoff all of the leds and back to start")
                    # print ("loop start: Wait for 1st input...")
                    break
                elif D_triggered and C_triggered==False:
                    TriggeredAllFalse()
                    if RPi.GPIO.input(LED3):
                        turnoff123()
                        print("２番目の入力==[Button D],キー==[CD](True),LED123を消す。最初に戻る。")
                        # print("2nd input=[Button D],True,turnoff all of the leds and back to start")
                        pass
                    elif RPi.GPIO.input(LED2):
                        turnon(LED3)
                        print("２番目の入力==[Button D],キー==[CD](True),LED3をつける。最初に戻る。")
                        # print("2nd input=[Button D],True,turn on LED 3 and back to start")
                    elif RPi.GPIO.input(LED1):
                        turnon(LED2)
                        print("２番目の入力==[Button D],キー==[CD](True),LED2をつける。最初に戻る。")
                        # print("2nd input=[Button D],True,turn on LED 2 and back to start")
                    elif RPi.GPIO.input(LED1)==False:
                        turnon(LED1)
                        print("２番目の入力==[Button D],キー==[CD](True),LED1をつける。最初に戻る。")
                        # print("2nd input=[Button D],True,turn on LED 1 and back to start")
                    print ("１番目の入力を待つ...")
                    #print ("loop start: Wait for 1st input...")
                    break
                elif C_triggered==True and D_triggered==True:
                    TriggeredAllFalse()
                    turnoff123()
                    print("２番目の入力==[Error],キー==[Error],最初に戻る。")
                    time.sleep(0.3)
                    print ("１番目の入力を待つ...")
                    # print("2nd input==Wrong,turnoff all of the leds and back to start")
                    # print ("loop start: Wait for 1st input...")
                    break
                else:
                    continue
                pass

        elif D_triggered and C_triggered==False:        ### when 1stinput is D
            TriggeredDllFalse()
            turnoff123()
            print("１番目の入力==[Button D],キー==[D](False),LED123を消す。最初に戻る。")
            time.sleep(0.3)
            print ("１番目の入力を待つ...")
            # print("1st input=[Button D],False,back to start")
            # print("loop start: Wait for 1st input...")
            continue

        else:
            TriggeredAllFalse()
            continue

finally:                   # this block will run no matter how the try block exits
    RPi.GPIO.cleanup()         # clean up after yourself
