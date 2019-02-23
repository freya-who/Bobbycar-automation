#from gpiozero import Servo
#import time
#
#my_servo = Servo(18)
#
#try:
#    while True:
#        print('servo 1')
#        my_servo.value = 1        
#        time.sleep(2)
#        print('servo 0')
#        my_servo.value = 0    
#        time.sleep(2)
#        print('servo -1')
#        my_servo.value = -1    
#        time.sleep(2)
#except KeyboardInterrupt:
#    my_servo.close()

#import RPi.GPIO as GPIO
#import time
#
#servoPIN = 18
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(servoPIN, GPIO.OUT)
#
#p = GPIO.PWM(servoPIN, 50) # GPIO 17 als PWM mit 50Hz
#p.start(2.5) # Initialisierung
#try:
#  while True:
#    p.ChangeDutyCycle(5)
#    time.sleep(0.5)
#    p.ChangeDutyCycle(7.5)
#    time.sleep(0.5)
#    p.ChangeDutyCycle(12.5)
#    time.sleep(0.5)
#    p.ChangeDutyCycle(2.5)
#    time.sleep(0.5)
#except KeyboardInterrupt:
#  p.stop()
#  GPIO.cleanup()

import pigpio
from time import sleep

# connect to the 
pi = pigpio.pi()

# loop forever
try:
    while True:
        pi.set_servo_pulsewidth(18, 0)    # off
        sleep(1)
        pi.set_servo_pulsewidth(18, 1000) # position anti-clockwise
        sleep(1)
        pi.set_servo_pulsewidth(18, 1500) # middle
        sleep(1)
        pi.set_servo_pulsewidth(18, 2000) # position clockwise
        sleep(1)
except KeyboardInterrupt:
  pi.stop()
