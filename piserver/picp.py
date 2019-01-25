#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scripts import boardop
import RPi.GPIO
import smbus
import time

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

bp = Blueprint('picp', __name__ ,url_prefix='/picp')



@bp.route('/')
def index():
	print ("进入picp，index()方法")
	boardop.init()
	boardop.turnon(boardop.LED0)
	return render_template('index.html')

@bp.route("test",methods=['POST'])
def test():
	print ("进入路由test，方法test打印")

	return "post 返回值：进入test返回"
#拉高低电平
@bp.route("pullupgpio/<pinname>",methods=['POST']) #gpio是部件名称（boardop里的gpio变量），不是数字。。。
def pullupgpio(pinname):
	print ("进入路由pullupGPIO，方法pullupGPIO打印")
	#boardop.turnon(boardop.LED0)
	print(boardop.getPIN_NUM(pinname)) #得到部件名称的GPIO编号
	boardop.turnon(boardop.getPIN_NUM(pinname))
	return "post  戻り値："+pinname.encode("utf-8")+"==True"

@bp.route("pulldowngpio/<pinname>",methods=['POST'])
def pulldowngpio(pinname):
	print ("路由：pulldownGPIO，方法pulldownGPIO打印")
	print ("参数GPIO值：")
	print (pinname)
	print(boardop.getPIN_NUM(pinname))
	boardop.turnoff(boardop.getPIN_NUM(pinname))
	return "post 戻り値："+pinname.encode("utf-8")+"==False"
	# return "post  戻り値：LED0==OFF,GPIO13==False  >>>>>> LED0消灯"

#马达操作，控制马达方向
@bp.route("motord1",methods=['POST'])
def motord1():
	print ("路由：motord1，方法rotatemotor1打印")
	boardop.turnon(boardop.In1_Motor)
	boardop.turnoff(boardop.In2_Motor)

	return "post  戻り値：モーター正回転  GPIO13==True  GPIO19==False"

@bp.route("motord2",methods=['POST'])
def motord2():
	print ("路由：motord2，方法rotatemotor2")
	boardop.turnon(boardop.In2_Motor)
	boardop.turnoff(boardop.In1_Motor)

	return "post  戻り値：モーター逆回転  GPIO13==False  GPIO19==True"

@bp.route("motorstop",methods=['POST'])
def motorstop():
	print ("路由：motorstop，方法motorstop")
	boardop.turnoff(boardop.In1_Motor)
	boardop.turnoff(boardop.In2_Motor)

	return "post  戻り値：モーター停止  GPIO13==False  GPIO19==False"

@bp.route("motorautorun/<command>",methods=['POST']) #自动控制马达
def motorautorun(command): #command stop(0) or run(1) 
	print ("路由：motorautorun，方法motorautorun")
	if command=="1":  #自动运行开始
		print"进入command==1"
		t1=float(str(request.form.get("t1")))
		t2=float(str(request.form.get("t2")))
		t3=float(str(request.form.get("t3")))
		t4=float(str(request.form.get("t4")))
		t5=float(str(request.form.get("t5")))
		t6=float(str(request.form.get("t6")))
		t7=float(str(request.form.get("t7")))
		t8=float(str(request.form.get("t8")))
		print ("t1==%s"%t1)
		print ("t2==%s"%t2)
		print ("t3==%s"%t3)
		print ("t4==%s"%t4)
		print ("t5==%s"%t5)
		print ("t6==%s"%t6)
		print ("t7==%s"%t7)
		print ("t8==%s"%t8)

		boardop.turnon(boardop.In1_Motor)
		boardop.turnoff(boardop.In2_Motor)
		time.sleep(t1)
		boardop.turnoff(boardop.In1_Motor)
		boardop.turnoff(boardop.In2_Motor)
		time.sleep(t2)

		boardop.turnon(boardop.In1_Motor)
		boardop.turnoff(boardop.In2_Motor)
		time.sleep(t3)
		boardop.turnoff(boardop.In1_Motor)
		boardop.turnoff(boardop.In2_Motor)
		time.sleep(t4)
	#反向旋转
		boardop.turnon(boardop.In2_Motor)
		boardop.turnoff(boardop.In1_Motor)
		time.sleep(t5)
		boardop.turnoff(boardop.In1_Motor)
		boardop.turnoff(boardop.In2_Motor)
		time.sleep(t6)
	    
		boardop.turnon(boardop.In2_Motor)
		boardop.turnoff(boardop.In1_Motor)
		time.sleep(t7)
		boardop.turnoff(boardop.In1_Motor)
		boardop.turnoff(boardop.In2_Motor)
		time.sleep(t8)
	if command=="0":
		print("进入command==0，自动运行停止")
		boardop.turnoff(boardop.In1_Motor)
		boardop.turnoff(boardop.In2_Motor)

 
	return "post  戻り値：モーター自動運転完了　運転時間:"+str(t1+t2+t3+t4+t5+t6+t7+t8)+"s "

# +" t2=="+t2+" t3=="+t3+" t4=="+t4+" t5=="+t5+" t6=="+t6+" t7=="+t7+" t8=="+t8
# #刷新温度
# @bp.route("t_refresh",methods=['POST'])
# def t_refresh():
# 	print ("路由：t_refresh，方法t_refresh")
# 	bus = smbus.SMBus(1)
# 	address_adt7410 = 0x48
# 	register_adt7410 = 0x00
# 	Temperature=boardop.read_adt7410()
# 	print ("温度Temerature==")
# 	print (Temperature)

# 	result=str(Temperature)
# 	return result