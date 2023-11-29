#coding:utf8
import RPi.GPIO as GPIO
import time

def init():
     GPIO.setwarnings(False)
     GPIO.setmode(GPIO.BCM)
     GPIO.setup(17,GPIO.OUT)
     GPIO.setup(27,GPIO.IN)
     pass
def beep():
      for i in range(1,6):
                    GPIO.output(17,GPIO.LOW)
                    time.sleep(0.5)
                    GPIO.output(17,GPIO.HIGH)
                    time.sleep(0.5)
                    print("the LED is FLASHING")

def detct():
       for i in range(1,31):
             if GPIO.input(27) == True:
                 GPIO.output(17,GPIO.LOW)
                 print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"  Someone is closing!")
                 beep()
             else:
                 GPIO.output(17,GPIO.HIGH)
                 print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"  Noanybody!")
                 time.sleep(6) #每6秒检查一次
time.sleep(2)
init()
detct()
GPIO.cleanup()


