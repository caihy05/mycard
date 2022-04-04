# coding:utf-8
import RPi.GPIO as GPIO
import time
import sys
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
from tornado.options import define,options

#GPIO.setmode(GPIO.BOARD)
define("port",default=8080,help="run on the given port",type=int)
# 电机接口定义
ENA = 32	#//L298使能A
ENB = 33	#//L298使能B
IN1 = 11	#//电机接口1
IN2 = 16	#//电机接口2
IN3 = 13	#//电机接口3
IN4 = 15	#//电机接口4

# 初始化
GPIO.setmode(GPIO.BOARD)
def init():
    # GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ENA,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
    pwmA = GPIO.PWM(ENA,200)          #200HZ 
    pwmA.start(20) #产生占空比为0.2的PWM信号，取值范围0-100, 默认值取0.2
    #右边
    GPIO.setup(ENB,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)

pwmA = GPIO.PWM(ENA,200)          #200HZ 
pwmA.start(20) #产生占空比为0.2的PWM信号，取值范围0-100, 默认值取0.2

pwmB = GPIO.PWM(ENB,200)          #200HZ 
pwmB.start(20) #产生占空比为0.2的PWM信号，取值范围0-100,默认值取0.2

# 前进w、后退s、左转a、右转d、加速u、减速l、刹车x|(速度20-60, 0、1、2、3、4)
# 前进w
def forward():
    print("前进w")
    # 前进修改占空比为默认0.2的PWM信号
    pwmA.ChangeDutyCycle(0.2)
    GPIO.output(IN1,True)
    GPIO.output(IN2,False)
    pwmB.ChangeDutyCycle(0.2)
    GPIO.output(IN3,True)
    GPIO.output(IN4,False)

# 后退s
def back():
    print("后退s")
    # 前进修改占空比为默认0.2的PWM信号
    pwmA.ChangeDutyCycle(0.2)
    GPIO.output(IN1,False)
    GPIO.output(IN2,True)
    pwmB.ChangeDutyCycle(0.2)
    GPIO.output(IN3,False)
    GPIO.output(IN4,True)
# 刹车x
def stop():
    print("刹车x")
    GPIO.output(IN1,False)
    GPIO.output(IN2,False)
    GPIO.output(IN3,False)
    GPIO.output(IN4,False)
# 这里先low一点一个正转一个反转
# 左转a
def left():
    print("左转a")
    pwmA.ChangeDutyCycle(0.2)
    GPIO.output(IN1,False)
    GPIO.output(IN2,True)
    pwmB.ChangeDutyCycle(0.2)
    GPIO.output(IN3,True)
    GPIO.output(IN4,False)
# 右转d
def right():
    print("右转d")
    pwmA.ChangeDutyCycle(0.2)
    GPIO.output(IN1,True)
    GPIO.output(IN2,False)
    pwmB.ChangeDutyCycle(0.2)
    GPIO.output(IN3,False)
    GPIO.output(IN4,True)
# 加速u
def upSpeed():
    print("加速u")
    pwmA.ChangeDutyCycle(0.2+0.1)
    pwmB.ChangeDutyCycle(0.2+0.1) 

# 减速l
def lowSpeed():
    print("减速l")
    pwmA.ChangeDutyCycle(0.2-0.1)
    pwmB.ChangeDutyCycle(0.2-0.1) 


class XiaocheHandler(tornado.web.RequestHandler):
    def get(self):
            self.render("xiaoche.html")
    def post(self):
            init()
            # sleep_time=0.1
            arg=self.get_argument('k')
            # arg=self.get_argument('k')
            if(arg=='w'):
                forward()
            elif(arg=='s'):
                back()
            elif(arg=='a'):
                left()
            elif(arg=='d'):
                right()
            elif(arg=='x'):
                stop()
            elif(arg=='u'):
                upSpeed()
            elif(arg=='l'):
                lowSpeed()
            else:
                return False
            self.write(arg)
if __name__ == '__main__':
    # pass
    while 1:
        xc = XiaocheHandler()
        cmd = input('前进w、后退s、左转a、右转d、变速u、刹车x')
        if cmd == "w":
            xc.forward()
        elif cmd == "s":
            xc.back()
        elif cmd == "a": 
            xc.left()
        elif cmd == "d":
            xc.right()
        elif cmd == "u":
            xc.upSpeed()
        elif cmd == "l":
            xc.lowSpeed()
        elif cmd == "x":
            xc.stop()
        else:
            pass