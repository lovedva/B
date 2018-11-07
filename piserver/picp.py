#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scripts import iniboard
import RPi.GPIO

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

bp = Blueprint('picp', __name__ ,url_prefix='/picp')

RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(iniboard.LED0, RPi.GPIO.OUT)

@bp.route('/')
def index():
	print ("进入picp，index()方法")
	iniboard.init()
#	iniboard.turnon(iniboard.LED0)
	return render_template('index.html')

@bp.route("test",methods=['POST'])
def test():
	print ("进入路由test，方法test打印")

	return "post\n返回值：进入test返回"
#拉高低电平
@bp.route("pullupgpio/<gpio>",methods=['POST'])
def pullupgpio(gpio):
	print ("进入路由pullupGPIO，方法pullupGPIO打印")
	iniboard.turnon(iniboard.LED0)
	print(iniboard.getPIN_NUM(gpio))
	iniboard.turnon(iniboard.getPIN_NUM(gpio))
	return "post\n戻り値："+gpio.encode("utf-8")+"==True"

@bp.route("pulldowngpio/<gpio>",methods=['POST'])
def pulldowngpio(gpio):
	print ("路由：pulldownGPIO，方法pulldownGPIO打印")
	print ("参数GPIO值：")
	print (gpio)
	print(iniboard.getPIN_NUM(gpio))
	iniboard.turnoff(iniboard.getPIN_NUM(gpio))
	return "post\n戻り値："+gpio.encode("utf-8")+"==False"
	# return "post\n戻り値：LED0==OFF,GPIO13==False\n>>>>>> LED0消灯"

#旋转马达，控制马达方向
@bp.route("motord1",methods=['POST'])
def motord1():
	print ("路由：motord1，方法rotatemotor1打印")
	iniboard.turnon(iniboard.In1_Motor)
	iniboard.turnoff(iniboard.In2_Motor)

	return "post\n戻り値：モーター正回転\nGPIO13==True\nGPIO19==False"

@bp.route("motord2",methods=['POST'])
def motord2():
	print ("路由：motord2，方法rotatemotor2")
	iniboard.turnon(iniboard.In2_Motor)
	iniboard.turnoff(iniboard.In1_Motor)

	return "post\n戻り値：モーター逆回転\nGPIO13==False\nGPIO19==True"

@bp.route("motorstop",methods=['POST'])
def motorstop():
	print ("路由：motorstop，方法motorstop")
	iniboard.turnoff(iniboard.In1_Motor)
	iniboard.turnoff(iniboard.In2_Motor)

	return "post\n戻り値：モーター停止\nGPIO13==False\nGPIO19==False"