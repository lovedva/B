#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import RPi.GPIO
import sys
import adt7410

class PIinit:
	"初始化板子参数设定"
	flag=0

	#设置输出PIN
	LED0=6  #程序开始指示灯
	TempOUT1=12

	def __init__(self):
		RPi.GPIO.setmode(RPi.GPIO.BCM)
		RPi.GPIO.setup(PIinit.LED0, RPi.GPIO.OUT)
		RPi.GPIO.setup(PIinit.TempOUT1, RPi.GPIO.OUT)
		RPi.GPIO.output(PIinit.LED0, True) #点亮LED0
		print ("进入__init__方法")

class pidCtr:
	"PID控制器"
	flag=1
	Sv=50.000 #用户输入
	Pv=0.000
	T=500.000 #ms PID计算周期
	Kp=42.000 #比例系数
	Ti=60000.000 #ms 积分时间
	Td=1000.000 #ms 微分时间
	Ek=0.000 #本次偏差
	Ek_1=0.000 #上次偏差
	SEk=0.000 #历史偏差总和
	Iout=0.000
	Pout=0.000
	Dout=0.000
	OUT0=1.000
	OUT=0.000
	pwmcyle=200 #ms PWM周期

	def calc(self):
		self.Ek=self.Sv-self.Pv #计算当前偏差
		# print("Ek==%s"%self.Ek)
		# print("Ek_1==%s"%self.Ek_1)
		self.Pout=self.Kp*self.Ek  #1-比例项输出
		print("Pout==%s"%self.Pout)
		self.SEk+=self.Ek  #历史偏差总和
		# print("SEk==%s"%self.SEk)
		DeltaEK=self.Ek-self.Ek_1  #上一次和本次的偏差之差
		ti=self.T/self.Ti  #pid周期/积分时间
		# print("ti==%s"%ti)
		Ki=ti*self.Kp  #积分系数
		# print("Ki==%s"%Ki)
		self.Iout=Ki*self.SEk #2-积分输出
		print("Iout==%s"%self.Iout)
		td=self.Td/self.T #微分时间/pid周期
		Kd=self.Kp*td #微分系数
		self.Dout=Kd*DeltaEK #3-微分项输出
		print("Dout==%s"%self.Dout)
		out=self.Pout+self.Iout+self.Dout+self.OUT0 #4-pid计算结果
		print("calc.out==%s"%out)
		#pid计算结果处理‘’
		if out>self.pwmcyle:
			self.OUT=self.pwmcyle
		elif out<0:
			self.OUT=0
		elif 0<=out<=self.pwmcyle:
			self.OUT=out
		self.Ek_1=self.Ek 


if __name__ == "__main__":
	try:
		pi=PIinit()
		print("初始化完毕，创建PIinit对象pi，flag==%s"%pi.flag)
		# RPi.GPIO.output(pi.TempOUT1, True)
		# print("TempOUT1开始输出1")
		pid=pidCtr()
		print("创建pidCtr对象pid，flag==%s"%pid.flag)
		#设置pwm
		pwm=RPi.GPIO.PWM(pi.TempOUT1,5)#pwm周期200ms
		pwm.start(1)
		file_handle=open('Templog.txt',mode='w')
		while True:
			pid.Pv=adt7410.read_adt7410()  
			print("今回の温度==%s度"%pid.Pv)
			file_handle.write("%s | "%pid.Pv)
			pid.calc()
			print("pidCr.OUTの計算結果==%s"%pid.OUT)
			dc=pid.OUT/pid.pwmcyle*100
			pwm.ChangeDutyCycle(dc)
			print("PWM信号のDutyCyle：%s"%dc)
			file_handle.write("%s ;\n"%dc)
			print("-----------------------------")
			time.sleep(0.5)
			pass
			
		file_handle.close()
	except Exception as e:
		raise
	else:
		pass
	finally:
		file_handle.close()
		RPi.GPIO.cleanup()
	