#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO
import time
from multiprocessing import Process
import multiprocessing as mp
import json
from flask import send_from_directory
import os
from scripts import boardop,pt1000,ads1248,pid60Ctr,pid70Ctr,pid90Ctr

from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for,jsonify
)

bp = Blueprint('cp', __name__ ,url_prefix='/cp')

RPi.GPIO.setmode(RPi.GPIO.BCM)
# LED0=17  #GPIO for UC
# In1_Motor=13   #GPIOXX 
# In2_Motor=19
TempOUT1=14 #60度
TempOUT2=23 #70度
TempOUT3=16 #90度

# RPi.GPIO.setup(LED0, RPi.GPIO.OUT)
# RPi.GPIO.setup(In1_Motor, RPi.GPIO.OUT)
# RPi.GPIO.setup(In2_Motor, RPi.GPIO.OUT)
RPi.GPIO.setup(TempOUT1, RPi.GPIO.OUT)
RPi.GPIO.setup(TempOUT2, RPi.GPIO.OUT)
RPi.GPIO.setup(TempOUT3, RPi.GPIO.OUT)

ads1248.init()
boardop.turnon(3) #conversation start

#绑定进程方法
cw=0
ccw=0
stp=0
process=None
ph1=None
ph2=None
ph3=None
pwm1=RPi.GPIO.PWM(TempOUT1,5)#pwm周200ms
pwm2=RPi.GPIO.PWM(TempOUT2,5)#pwm周200ms
pwm3=RPi.GPIO.PWM(TempOUT3,5)#pwm周200ms
pid60=pid60Ctr.pidCtr()
pid70=pid70Ctr.pidCtr()
pid90=pid90Ctr.pidCtr()
print "pid60:"+str(pid60.Pv)
temp1=mp.Value('d',11.11)
temp2=mp.Value('d',22.22)
temp3=mp.Value('d',33.33)


def mrun():
	global cw
	global ccw
	global stp
	boardop.turnon(boardop.In1_Motor)
	boardop.turnoff(boardop.In2_Motor)
	time.sleep(cw)
	boardop.turnon(boardop.In2_Motor)
	boardop.turnoff(boardop.In1_Motor)
	time.sleep(ccw)
	boardop.turnoff(boardop.In1_Motor)
	boardop.turnoff(boardop.In2_Motor)
	time.sleep(stp)
	print "mrun finished"

def mautorun(timelist,loop):
	loop=int(loop)
	for i in range (1,loop+1):
		print str(i)+"次"
		for item in timelist:
			boardop.turnon(boardop.In1_Motor)
			boardop.turnoff(boardop.In2_Motor)
			time.sleep(float(item.get('cw')))
			boardop.turnon(boardop.In2_Motor)
			boardop.turnoff(boardop.In1_Motor)
			time.sleep(float(item.get('ccw')))
			boardop.turnoff(boardop.In1_Motor)
			boardop.turnoff(boardop.In2_Motor)
			time.sleep(float(item.get('stp')))
	print "mautorun finished"

def heatup11(temp):
	print "heatup11,temp: "+str(temp)
	RPi.GPIO.setup(TempOUT1, RPi.GPIO.OUT)
	global pid60
	pid60.Sv=float(temp)
	global pwm1
	pwm1.start(1)
	global temp1
	file_handle1=open('60Templog.txt',mode='w')
	while True:
		print "heatup11,target temp: "+str(temp)
		pid60.Pv=float(pt1000.calcTemp(01))
		temp1.value=pid60.Pv
		print "temp1:"+str(temp1)
		pid60.calc()
		dc1=pid60.OUT/pid60.pwmcycle*100
		print "dc1 "+str(dc1)
		pwm1.ChangeDutyCycle(dc1)
		print("Pt1000で測温[01]==%s\n-----------------------------"%pid60.Pv)
		file_handle1.write("%s \n"%pid60.Pv)

def heatup22(temp):
	print "heatup22,temp: "+str(temp)
	RPi.GPIO.setup(TempOUT2, RPi.GPIO.OUT)
	global pid70
	pid70.Sv=float(temp)
	global pwm2
	pwm2.start(1)
	file_handle1=open('70Templog.txt',mode='w')
	while True:
		print "heatup22,target temp: "+str(temp)
		pid70.Pv=float(pt1000.calcTemp(23))
		global temp1
		temp2.value=pid70.Pv
		pid70.calc()
		dc1=pid70.OUT/pid70.pwmcycle*100
		print "dc1 "+str(dc1)
		pwm1.ChangeDutyCycle(dc1)
		print("Pt1000で測温[23]==%s\n-----------------------------"%pid70.Pv)
		file_handle1.write("%s \n"%pid70.Pv)

def heatup33(temp):
	print "heatup33,temp: "+str(temp)
	RPi.GPIO.setup(TempOUT3, RPi.GPIO.OUT)
	global pid90
	pid90.Sv=float(temp)
	global pwm3
	pwm3.start(1)
	file_handle1=open('90Templog.txt',mode='w')
	while True:
		print "heatup33,target temp: "+str(temp)
		pid90.Pv=float(pt1000.calcTemp(45))
		global temp3
		temp3.value=pid90.Pv
		pid90.calc()
		dc1=pid90.OUT/pid90.pwmcycle*100
		print "dc1 "+str(dc1)
		pwm1.ChangeDutyCycle(dc1)
		print("Pt1000で測温[45]==%s\n-----------------------------"%pid90.Pv)
		file_handle1.write("%s \n"%pid90.Pv)


#路由
@bp.route('/')
def index():
	print ("进入cp，index()方法")
	boardop.init()
	boardop.turnon(boardop.LED0)
	return render_template('index.html')

#拉高低电平
@bp.route("pullupgpio/<pinname>",methods=['POST','get']) #gpio是部件名称（boardop里的gpio变量），不是数字。。。
def pullupgpio(pinname):
	print ("进入路由pullupGPIO，方法pullupGPIO打印")
	#boardop.turnon(boardop.LED0)
	print(boardop.getPIN_NUM(pinname)) #得到部件名称的GPIO编号
	boardop.turnon(boardop.getPIN_NUM(pinname))
	return "LED0 ON, GPIO17==True "

@bp.route("pulldowngpio/<pinname>",methods=['POST','get'])
def pulldowngpio(pinname):
	print ("路由：pulldownGPIO，方法pulldownGPIO打印")
	print ("参数GPIO值：")
	print (pinname)
	print(boardop.getPIN_NUM(pinname))
	boardop.turnoff(boardop.getPIN_NUM(pinname))
	return "LED0 OFF, GPIO17==False "
	# return "post  戻り値：LED0==OFF,GPIO13==False  >>>>>> LED0消灯"

# 显示温度
@bp.route("showtemps",methods=['POST','get'])
def showtemps():
	# print ("路由：showtemps打印")
	global temp1
	global temp2
	global temp3
	templist={'t1':temp1.value,'t2':temp2.value,'t3':temp3.value}
	print templist

	return jsonify(templist)
#加热
@bp.route("heatup1",methods=['GET','POST',])
def heatup1():
	data=request.json
	print(data)
	print("route heatup1, process ph1 start")
	global ph1
	ph1=Process(target=heatup11,args=(data.get('t1'),))
	ph1.start()
	return "Heater1 Tempreture="+str(data.get('t1'))

@bp.route("heatstop1",methods=['GET','POST',])
def heatstop1():
	print("route heatstop1,")
	global ph1
	ph1.terminate()
	global pwm1
	pwm1.stop()
	global temp1
	print "temp1 "+str(temp1)
	return "route heatstop1 finished"

@bp.route("heatup2",methods=['GET','POST',])
def heatup2():
	data=request.json
	print(data)
	print("route heatup2, process ph2 start")
	global ph2
	ph2=Process(target=heatup22,args=(data.get('t2'),))
	ph2.start()
	return "Heater2 Tempreture="+str(data.get('t2'))

@bp.route("heatstop2",methods=['GET','POST',])
def heatstop2():
	print("route heatstop2,")
	global ph2
	ph2.terminate()
	global pwm2
	pwm2.stop()
	return "route heatstop2 finished"

@bp.route("heatup3",methods=['GET','POST',])
def heatup3():
	data=request.json
	print(data)
	print("route heatup3, process ph3 start")
	global ph3
	ph3=Process(target=heatup33,args=(data.get('t3'),))
	ph3.start()
	return "Heater3 Tempreture="+str(data.get('t3'))

@bp.route("heatstop3",methods=['GET','POST',])
def heatstop3():
	print("route heatstop3,")
	global ph3
	ph3.terminate()
	global pwm3
	pwm3.stop()
	return "route heatstop3 finished"
	


#马达操作，控制马达方向
@bp.route("motord1",methods=['POST'])
def motord1():
	print ("路由：motord1，方法rotatemotor1打印")
	global cw
	print (cw)
	boardop.turnon(boardop.In1_Motor)
	boardop.turnoff(boardop.In2_Motor)

	return "GPIO13==True GPIO19==False"

@bp.route("motord2",methods=['POST'])
def motord2():
	print ("路由：motord2，方法rotatemotor2")
	boardop.turnon(boardop.In2_Motor)
	boardop.turnoff(boardop.In1_Motor)

	return "GPIO13==False GPIO19==True"

@bp.route("motorstop",methods=['POST'])
def motorstop():
	print ("路由：motorstop，方法motorstop")
	boardop.turnoff(boardop.In1_Motor)
	boardop.turnoff(boardop.In2_Motor)

	return "GPIO13==False\nGPIO19==False"

@bp.route("motorrun",methods=['POST'])
def motorrun():
	data=request.json
	print(data)
	tcw=float(data.get('cw'))
	tccw=float(data.get('ccw'))
	tstp=float(data.get('stp'))
	print("cw "+str(tcw))
	print("ccw "+str(tccw))
	print("stp "+str(tstp))
	global cw
	cw=tcw
	global ccw
	ccw=tccw
	global stp
	stp=tstp
	total=cw+ccw+stp
	p = Process(target=mrun)
	global process
	process=p
	process.start()
	process.join()
	print "route over"

	# return "request finished: cw "+str(data.get('cw'))+" ccw "+str(data.get('ccw'))+" stp "+str(data.get('stp')
	return "request finished: cw "+str(cw)+" ccw "+str(ccw)+" stp "+str(stp)+" total "+str(total)

@bp.route("motorautostp",methods=['GET'])
def motorautostp():
	global process
	process.terminate()
	return "motorautostp request finished"

@bp.route("motorautorun/<loop>",methods=['POST'])
def motorautorun(loop):
	RPi.GPIO.setmode(RPi.GPIO.BCM)
	data=request.json
	print(data)
	timelist=data.get('timelist')
	print("Cw "+str(data.get('timelist')[0].get('cw')))
	print("timelist长度 "+str(len(timelist)))
	loop=int(loop)
	p = Process(target=mautorun,args=(timelist,loop))
	global process
	process=p
	process.start()
	process.join()
	print "route motorautorun over"
	
	return str(len(timelist))+" data rows, loop "+str(loop)+" times\n "+str(timelist)


@bp.route("savemotortime",methods=['POST'])
def savemotortime():
	data=request.json
	jsObj = json.dumps(data["timelist"])
	print(jsObj)  
	fileObject = open('motortime.json.txt', 'w')  
	fileObject.write(jsObj)  
	fileObject.close()  

	return "route savemotortimes request finished.\n file name: ' motortime.json.txt '"

@bp.route("exportmotortime/<t>",methods=['GET'])
def exportmotortime(t):
	print t
	print("enter route savemotortimes request ")
	return send_from_directory(os.getcwd(),filename="motortime.json.txt",as_attachment=True)

@bp.route("loadmotortime/<t>",methods=['GET'])
def loadmotortime(t):
	print t
	f=open('motortime.json.txt')
	
	print("enter route loadmotortimes request ")
	return jsonify(f.read())

@bp.route("loadtempdata/<t>",methods=['GET'])
def loadtempdata(t):
	# print t
	f1=open('60Templog.txt')
	f2=open('70Templog.txt')
	f3=open('90Templog.txt')
	
	print("enter route loadtempdata  ")
	return jsonify({"f1":f1.read(),"f2":f2.read(),"f3":f3.read()})

