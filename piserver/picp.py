#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scripts import boardop
import RPi.GPIO
import smbus

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

	return "post\n返回值：进入test返回"
#拉高低电平
@bp.route("pullupgpio/<pinname>",methods=['POST']) #gpio是部件名称（boardop里的gpio变量），不是数字。。。
def pullupgpio(pinname):
	print ("进入路由pullupGPIO，方法pullupGPIO打印")
	#boardop.turnon(boardop.LED0)
	print(boardop.getPIN_NUM(pinname)) #得到部件名称的GPIO编号
	boardop.turnon(boardop.getPIN_NUM(pinname))
	return "post\n戻り値："+pinname.encode("utf-8")+"==True"

@bp.route("pulldowngpio/<pinname>",methods=['POST'])
def pulldowngpio(pinname):
	print ("路由：pulldownGPIO，方法pulldownGPIO打印")
	print ("参数GPIO值：")
	print (pinname)
	print(boardop.getPIN_NUM(pinname))
	boardop.turnoff(boardop.getPIN_NUM(pinname))
	return "post\n戻り値："+pinname.encode("utf-8")+"==False"
	# return "post\n戻り値：LED0==OFF,GPIO13==False\n>>>>>> LED0消灯"

#马达操作，控制马达方向
@bp.route("motord1",methods=['POST'])
def motord1():
	print ("路由：motord1，方法rotatemotor1打印")
	boardop.turnon(boardop.In1_Motor)
	boardop.turnoff(boardop.In2_Motor)

	return "post\n戻り値：モーター正回転\nGPIO13==True\nGPIO19==False"

@bp.route("motord2",methods=['POST'])
def motord2():
	print ("路由：motord2，方法rotatemotor2")
	boardop.turnon(boardop.In2_Motor)
	boardop.turnoff(boardop.In1_Motor)

	return "post\n戻り値：モーター逆回転\nGPIO13==False\nGPIO19==True"

@bp.route("motorstop",methods=['POST'])
def motorstop():
	print ("路由：motorstop，方法motorstop")
	boardop.turnoff(boardop.In1_Motor)
	boardop.turnoff(boardop.In2_Motor)

	return "post\n戻り値：モーター停止\nGPIO13==False\nGPIO19==False"

@bp.route("motorautorun",methods=['POST']) #自动控制马达
def motorautorun():
	print ("路由：motorautorun，方法motorautorun")
	t1=request.form.get("t1")
	print "t1=="+t1

	return "post\n戻り値：モーター停止\nGPIO13==False\nGPIO19==False"


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