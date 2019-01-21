#!/usr/bin/env python
# -*- coding: utf-8 -*-
#热电传感器控制数字电位器
import time
import RPi.GPIO
import X9C503P as digipot
import E6B2_CWZ6C as encoder 

# 设置全局变量 setup global variables at first
# setup input pins,edit pin number here
InputA=16  #GPIO16 为A输入
InputB=7   #GPIO7 为B输入
InputC=8   #GPIO8 为C输入
InputD=15  #GPIO15 as inputD


# setup GPIO triggered  记录按钮输入状态（是否按下）
A_triggered= False
B_triggered= False
C_triggered= False
D_triggered= False

RPi.GPIO.setup(InputA, RPi.GPIO.IN,pull_up_down=RPi.GPIO.PUD_DOWN)
RPi.GPIO.setup(InputB, RPi.GPIO.IN,pull_up_down=RPi.GPIO.PUD_DOWN)
RPi.GPIO.setup(InputC, RPi.GPIO.IN,pull_up_down=RPi.GPIO.PUD_DOWN)
RPi.GPIO.setup(InputD, RPi.GPIO.IN,pull_up_down=RPi.GPIO.PUD_DOWN)

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

# when a rising edge is detected on pin,the callback functions will be run
RPi.GPIO.add_event_detect(InputA, RPi.GPIO.RISING,callback=SwitchA,bouncetime=200 ) # when use real button swtich to switch the input level,
RPi.GPIO.add_event_detect(InputB, RPi.GPIO.RISING,callback=SwitchB,bouncetime=200 ) # bouncetime=[time] to debounce the switch.
RPi.GPIO.add_event_detect(InputC, RPi.GPIO.RISING,callback=SwitchC,bouncetime=200 )
RPi.GPIO.add_event_detect(InputD, RPi.GPIO.RISING,callback=SwitchD,bouncetime=200 )

try:
    start = time.time()
    digipot.init()
    print(" 焦電素子：InputA=16 InputB=7  GPIO7 InputC=8 InputD=15")
    print(" rotary encoder ：encoderOUTA=27 encoderOUTB=17 encoderOUTZ=26")
    print（" digipot :CS=13   INC=11  UD=22 "）
    print ("AltとCを押すと,プログラムを中止する。")
    time.sleep(0.5)
    print ("ループ開始：１番目の入力を待つ... Wait for 1st input...")

    #主循环开始,第一次循环
    while True:
        time.sleep(0.01)
        pass
        #检测第一次输入A，第一次循环
        if A_triggered and B_triggered==False:
            TriggeredAllFalse()
            print("第一次输入：A==Rising,B==0,等待第二次输入。。")

            #第二次循环
            while True:
                time.sleep(0.1)
            #检测第二次输入BCD，循环2
                if B_triggered or C_triggered or D_triggered:
                    print("２番目の入力==[Input B/C/D],キー==[A B/C/D](down),turn off cs")
                        digipot.turnoff(digipot.CS)
                        time.sleep(0.3)
                        print ("3番目の入力を待つ...(pyroelectric only)")
                        TriggeredAllFalse()

                        #第三次循环
                        while True:
                            time.sleep(0.01)
                            #检测第三次输入A 
                            if A_triggered:
                                TriggeredAllFalse()
                                print("3番目の入力==[Input A],キー==[A ](),wait for 4th input(pyroelectric only)")
                                #第四次循环，检测输入B/C/D
                                while True:
                                    time.sleep(0.01)
                                    pass
                                    if B_triggered or C_triggered or D_triggered:
                                        print("4番目の入力==[Input B/C/D],キー==[A B/C/D](down),pull up digipot")
                                        digipot.turnon(digipot.UD)
                                        for i in range(0,24):
                                            digipot.turnon(digipot.INC)
                                            time.sleep(0.05)
                                            digipot.turnoff(digipot.INC)
                                        digipot.turnon(digipot.CS)
                                        TriggeredAllFalse()
                                        break #跳出第四次循环
                            elif B_triggered:
                                TriggeredAllFalse()
                                print("3番目の入力==[Input B],キー==[B ](),wait for 4th input(pyroelectric only)")
                                #第四次循环，检测输入B/C/D
                                while True:
                                    pass
                                    if A_triggered or C_triggered or D_triggered:
                                        print("4番目の入力==[Input A/C/D],キー==[B A/C/D](up),pull down digipot")
                                        digipot turnoff(digipot.UD)
                                        for i in range(0,24):
                                            digipot.turnon(digipot.INC)
                                            time.sleep(0.05)
                                            digipot.turnoff(digipot.INC)
                                        digipot.turnon(digipot.CS)
                                        TriggeredAllFalse()
                                        break #跳出第四次循环
                            break #跳出第三次循环
                break #跳出第二次循环

        #检测第一次输入为编码器输入eA
        if encoder.eA_triggered and encoder.eB_triggered==False:
            print("1番目の入力：eA==rise,B==0,2番目の入力を待っている。。。(rotary encoder only)")
            #第二次循环,
            while True:
                time.sleep(0.01)
                #检测第二次输入为eB
                if encoder.eB_triggered:
                    print("入力2==B rise，入力3を待っている。。。(rotary encoder only)")
                    #第三次循环，检测第三次输入为A下降
                    while True:
                        time.sleep(0.01)
                        if encoder.eA_triggered==False:
                            print("入力3==A fall，入力4を待っている。。。")
                            #第四次循环，检测第四次输入为B下降
                            while True:
                                pass
                                time.sleep(0.01)
                                if eB_triggered==False:
                                    print("入力4==B fall。回転方向： CW ,pull up digipot")
                                    digipot.turnon(digipot.UD)
                                    for i in range(0,24):
                                        digipot.turnon(digipot.INC)
                                        time.sleep(0.05)
                                        digipot.turnoff(digipot.INC)
                                    digipot.turnon(digipot.CS)
                                    TriggeredAllFalse()
                                    break #跳出第四次循环
                            break #退出第三次循环

                        #第三次循环，检测输入A/B
                        elif encoder.eB_triggered==False or encoder.eA_triggered:
                            print("入力3==B fall")
                                break #退出第三次循环
                        print("入力1に戻る，入力1を待っている。。。")
                        break #退出第二层循环

        #检测第一次循环输入为eB
        if encoder.eB_triggered and encoder.eA_triggered==False:
            print("1番目の入力：B==Rising,A==0,2番目の入力を待っている。。。")       
        #第二次输入为A升高            
            while True:
                time.sleep(TIME)
                if encoder.eA_triggered:
                    print("入力2==A rise，入力3を待っている。。。")
        #第三次输入为B下降
                    while True:
                        time.sleep(TIME)
                        if encoder.eB_triggered==False:
                            print("入力3==B fall，入力4を待っている。。。")
        #第四次输入为A下降
                            while True:
                                time.sleep(TIME)
                                if encoder.eA_triggered==False:
                                    print("入力4==A fall。回転方向： CWW pull down digipot ")
                                    digipot turnoff(digipot.UD)
                                    for i in range(0,24):
                                        digipot.turnon(digipot.INC)
                                        time.sleep(0.05)
                                        digipot.turnoff(digipot.INC)
                                    digipot.turnon(digipot.CS)
                                    TriggeredAllFalse()
                                    break #退出第四次循环
                            break  #退出第三次循环
    #第三次输入为A下降                                
                        elif encoder.eA_triggered==False or encoder.eB_triggered:
                            print("入力3==A fall")
                            break #退出第三次循环
                    print("入力1に戻る，入力1を待っている。。。")
                    break #退出第二层循环           
#第二次输入为B下降
                elif eB_triggered==False:
                    print("入力2==B fall")
                    print("入力1に戻る，入力1を待っている。。。")
                    break #退出第二次循环               
                    

except Exception as e:
    raise
else:
    pass
finally:
    RPi.GPIO.cleanup()