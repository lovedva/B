# -*- coding: utf-8 -*-

from multiprocessing import Process
import time
import os  
import sys 
import tty, termios 


def motorrun(args):
    for i in range (0,20):
        print("等待"+str(i)+"次")
        time.sleep(1)

p = Process(target=motorrun,args=('bob',))

if __name__ == '__main__':
    p.start()
    while True:
        fd=sys.stdin.fileno() 
        old_settings=termios.tcgetattr(fd) 
        try: 
            tty.setraw(fd) 
            ch=sys.stdin.read(1) 
        finally: 
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)  
        #print 'error' 
        if ch=='i': 
            print ('move forward')
        elif ch=='s':
            print ('start process')
            p.start() #报错，无法启动两次进程
        elif ch=='q': 
            print ("shutdown process p")
            p.terminate()
        elif ord(ch)==0x3: 
            #这个是ctrl c 
            print ("shutdown")
            break
        print ('press ctrl+c to quit')
        #rate.sleep()

