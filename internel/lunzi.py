#coding:utf-8
import RPi.GPIO as GPIO
import time

# 电机接口定义
ENA = 32	#//L298使能A
ENB = 33	#//L298使能B
IN1 = 11	#//电机接口1
IN2 = 16	#//电机接口2
IN3 = 13	#//电机接口3
IN4 = 15	#//电机接口4
GPIO.setmode(GPIO.BOARD)
# 初始化
# 左边
GPIO.setup(ENA,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
pwmA = GPIO.PWM(ENA,200)          #200HZ 
pwmA.start(20) #产生占空比为0.2的PWM信号，取值范围0-100%,默认值取20
#右边
GPIO.setup(ENB,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)
pwmB = GPIO.PWM(ENB,200)          #200HZ 
pwmB.start(20) #产生占空比为0.2的PWM信号，取值范围0-100%,默认值取20

# 前进1、后退2、左转3、右转4、变速5、刹车7|(速度20-60)
# 第一个参数：方向
class Lunzi():
    def __init__(self,n):
        self.dutyCycle = n
    # 前进1
    def forward(self):
        print("前进1")
        # 前进修改占空比为默认0.2的PWM信号
        pwmA.ChangeDutyCycle(0.2)
        GPIO.output(IN1,True)
        GPIO.output(IN2,False)
        pwmB.ChangeDutyCycle(0.2)
        GPIO.output(IN3,True)
        GPIO.output(IN4,False)

    # 后退2
    def back(self):
        print("后退2")
        # 前进修改占空比为默认0.2的PWM信号
        pwmA.ChangeDutyCycle(0.2)
        GPIO.output(IN1,False)
        GPIO.output(IN2,True)
        pwmB.ChangeDutyCycle(0.2)
        GPIO.output(IN3,False)
        GPIO.output(IN4,True)
    # 刹车7
    def stop(self):
        print("刹车7")
        GPIO.output(IN1,False)
        GPIO.output(IN2,False)
        GPIO.output(IN3,False)
        GPIO.output(IN4,False)
    # 这里先low一点一个正转一个反转
    # 左转3
    def left(self):
        print("刹车7")
        pwmA.ChangeDutyCycle(0.2)
        GPIO.output(IN1,False)
        GPIO.output(IN2,True)
        pwmB.ChangeDutyCycle(0.2)
        GPIO.output(IN3,True)
        GPIO.output(IN4,False)
    # 右转4
    def right(self):
        print("刹车7")
        pwmA.ChangeDutyCycle(0.2)
        GPIO.output(IN1,True)
        GPIO.output(IN2,False)
        pwmB.ChangeDutyCycle(0.2)
        GPIO.output(IN3,False)
        GPIO.output(IN4,True)
    # 变速5
    def changeSpeed(self):
        print("刹车7")
        pwmA.ChangeDutyCycle(0.2+0.1*self.dutyCycle)
        pwmB.ChangeDutyCycle(0.2+0.1*self.dutyCycle) 
