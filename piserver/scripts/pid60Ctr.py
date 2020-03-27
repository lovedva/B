#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import RPi.GPIO
import sys
import adt7410
import pt1000

class pidCtr:
    "PID控制器"
    flag=1  
    Sv=50.000 #用户输入
    Pv=0.000
    T=250 #ms PID计算周期
    Kp=20.000 #比例系数
    Ti=50000.000 #ms 积分时间
    Td=125.000 #ms 微分时间
    Ek=0.000 #本次偏差
    Ek_1=0.000 #上次偏差
    SEk=0.000 #历史偏差总和
    Iout=0.000
    Pout=0.000
    Dout=0.000
    OUT0=1.000
    OUT=0.000
    pwmcycle=200 #pwm输出周期

    def calc(self):    
        self.Ek=self.Sv-self.Pv #计算当前偏差
        # print("Ek==%s"%self.Ek)
        # print("Ek_1==%s"%self.Ek_1)
        self.Pout=self.Kp*self.Ek  #1-比例项输出
        # print("Pout==%s"%self.Pout)
        self.SEk+=self.Ek  #历史偏差总和
        # print("SEk==%s"%self.SEk)
        DeltaEK=self.Ek-self.Ek_1  #上一次和本次的偏差之差
        ti=self.T/self.Ti  #pid周期/积分时间
        # print("ti==%s"%ti)
        Ki=ti*self.Kp  #积分系数
        # print("Ki==%s"%Ki)
        self.Iout=Ki*self.SEk #2-积分输出
        # print("Iout==%s"%self.Iout)
        td=self.Td/self.T #微分时间/pid周期
        Kd=self.Kp*td #微分系数
        self.Dout=Kd*DeltaEK #3-微分项输出
        # print("Dout==%s"%self.Dout)
        # out=self.Pout+self.Iout+self.Dout+self.OUT0 #4-pid计算结果
        out=self.Pout
        # print("calc.out==%s"%out)
        #pid计算结果处理‘’
        if out>self.pwmcycle:
            self.OUT=self.pwmcycle
        elif out<0:
            self.OUT=0
        elif 0<=out<=self.pwmcycle:
            self.OUT=out
        self.Ek_1=self.Ek 


if __name__ == "__main__":
    try:

        print("初始化完毕，创建PIinit对象pi，flag==%s"%pi.flag)
        # RPi.GPIO.output(pi.TempOUT1, True)
        # print("TempOUT1开始输出1")
        pid=pidCtr()
        print("创建pidCtr对象pid，flag==%s"%pid.flag)
        #设置pwm
        pwm=RPi.GPIO.PWM(pi.TempOUT1,5)#pwm周期200ms
        pwm.start(1)
        file_handle=open('60Templog.txt',mode='w')
        while True:
            time.sleep(0.2)
            pid.Pv=max31855.sensor.readTempC()
            # pid.Pv=adt7410.read_adt7410()
            # pid.Pv=float(pt1000.calcTemp(4,5))
            print("Pt1000で測温[4,5]==%s \n"%pid.Pv)
            # sensortemp=adt7410.read_adt7410()
            # print("温度传感器测温==%s度"%sensortemp)
            file_handle.write("%s | "%pid.Pv)
            # file_handle.write("%s \n"%sensortemp)
            pid.calc()
            print("pidCr.OUTの計算結果==%s"%pid.OUT)
            dc=pid.OUT/pid.pwmcycle*100
            pwm.ChangeDutyCycle(dc)
            print("PWM信号のDutyCyle：%s"%dc)
            
            print("-----------------------------")
            
            pass
            
        file_handle.close()
    except Exception as e:
        raise
    else:
        pass
    finally:

        RPi.GPIO.cleanup()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import RPi.GPIO
import sys
import adt7410
import pt1000

class pidCtr:
    "PID控制器"
    flag=1  
    Sv=50.000 #用户输入
    Pv=0.000
    T=250 #ms PID计算周期
    Kp=20.000 #比例系数
    Ti=50000.000 #ms 积分时间
    Td=125.000 #ms 微分时间
    Ek=0.000 #本次偏差
    Ek_1=0.000 #上次偏差
    SEk=0.000 #历史偏差总和
    Iout=0.000
    Pout=0.000
    Dout=0.000
    OUT0=1.000
    OUT=0.000
    pwmcycle=200 #pwm输出周期

    def calc(self):    
        self.Ek=self.Sv-self.Pv #计算当前偏差
        # print("Ek==%s"%self.Ek)
        # print("Ek_1==%s"%self.Ek_1)
        self.Pout=self.Kp*self.Ek  #1-比例项输出
        # print("Pout==%s"%self.Pout)
        self.SEk+=self.Ek  #历史偏差总和
        # print("SEk==%s"%self.SEk)
        DeltaEK=self.Ek-self.Ek_1  #上一次和本次的偏差之差
        ti=self.T/self.Ti  #pid周期/积分时间
        # print("ti==%s"%ti)
        Ki=ti*self.Kp  #积分系数
        # print("Ki==%s"%Ki)
        self.Iout=Ki*self.SEk #2-积分输出
        # print("Iout==%s"%self.Iout)
        td=self.Td/self.T #微分时间/pid周期
        Kd=self.Kp*td #微分系数
        self.Dout=Kd*DeltaEK #3-微分项输出
        # print("Dout==%s"%self.Dout)
        # out=self.Pout+self.Iout+self.Dout+self.OUT0 #4-pid计算结果
        out=self.Pout
        # print("calc.out==%s"%out)
        #pid计算结果处理‘’
        if out>self.pwmcycle:
            self.OUT=self.pwmcycle
        elif out<0:
            self.OUT=0
        elif 0<=out<=self.pwmcycle:
            self.OUT=out
        self.Ek_1=self.Ek 


if __name__ == "__main__":
    try:

        print("初始化完毕，创建PIinit对象pi，flag==%s"%pi.flag)
        # RPi.GPIO.output(pi.TempOUT1, True)
        # print("TempOUT1开始输出1")
        pid=pidCtr()
        print("创建pidCtr对象pid，flag==%s"%pid.flag)
        #设置pwm
        pwm=RPi.GPIO.PWM(pi.TempOUT1,5)#pwm周期200ms
        pwm.start(1)
        file_handle=open('60Templog.txt',mode='w')
        while True:
            time.sleep(0.2)
            pid.Pv=max31855.sensor.readTempC()
            # pid.Pv=adt7410.read_adt7410()
            # pid.Pv=float(pt1000.calcTemp(4,5))
            print("Pt1000で測温[4,5]==%s \n"%pid.Pv)
            # sensortemp=adt7410.read_adt7410()
            # print("温度传感器测温==%s度"%sensortemp)
            file_handle.write("%s | "%pid.Pv)
            # file_handle.write("%s \n"%sensortemp)
            pid.calc()
            print("pidCr.OUTの計算結果==%s"%pid.OUT)
            dc=pid.OUT/pid.pwmcycle*100
            pwm.ChangeDutyCycle(dc)
            print("PWM信号のDutyCyle：%s"%dc)
            
            print("-----------------------------")
            
            pass
            
        file_handle.close()
    except Exception as e:
        raise
    else:
        pass
    finally:

        RPi.GPIO.cleanup()

    