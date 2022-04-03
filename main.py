cat << EOF > mycard.py
#coding:utf-8
"""
代码分三个部分：
1、电机控制
2、摄像头
3、主程序
"""
from socket import *
from time import ctime
import binascii
import RPi.GPIO as GPIO
import time
import threading

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

########电机驱动接口定义#################
ENA = 32	#//L298使能A
ENB = 33	#//L298使能B
IN1 = 11	#//电机接口1
IN2 = 16	#//电机接口2
IN3 = 13	#//电机接口3
IN4 = 15	#//电机接口4

#########电机初始化为LOW##########
GPIO.setup(ENA,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(ENB,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)

####PWM初始化，并设置频率为200HZ####
GPIO.setup(ENA,GPIO.OUT)	#初始化 
p1 = GPIO.PWM(ENA,200)          #200HZ 
p1.start(40) #产生占空比为0.4的PWM信号，取值范围0-100

#########定义电机正转函数##########
def gogo():
	print('motor gogo')
#	GPIO.output(ENA,True)
	GPIO.output(IN1,True)
	GPIO.output(IN2,False)

#########定义电机反转函数##########
def back():
	print("motor_back")
	GPIO.output(ENA,True)
	GPIO.output(IN1,False)
	GPIO.output(IN2,True)


#########定义电机停止函数##########
def stop():
	print('motor_stop')
	#GPIO.output(ENA,False)
	p1.stop # 停止PWM信号
	GPIO.output(ENB,False)
	GPIO.output(IN1,False)
	GPIO.output(IN2,False)
	GPIO.output(IN3,False)
	GPIO.output(IN4,False)	
	
'''
整个实验是
正转10.5s
反转10.5s
'''
while True:
	gogo();
	time.sleep(10.5)
	stop();
	time.sleep(10.1)
	back();
	time.sleep(10.5)

EOF