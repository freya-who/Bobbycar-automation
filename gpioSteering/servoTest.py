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
##p = GPIO.PWM(servoPIN, 50) # GPIO 17 als PWM mit 50Hz
##p.start(2.5) # Initialisierung
#try:
#  while True:
#    p.ChangeDutyCycle(5)
#    time.sleep(2)
#    p.ChangeDutyCycle(7.5)
#    time.sleep(2)
#    p.ChangeDutyCycle(12.5)
#    time.sleep(2)
#    p.ChangeDutyCycle(2.5)
#    time.sleep(2)
#except KeyboardInterrupt:
#  p.stop()
#  GPIO.cleanup()

#import RPi.GPIO as GPIO
#import time
#
#servoPIN = 18
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(servoPIN, GPIO.OUT)
#
##p = GPIO.PWM(servoPIN, 50) # GPIO 17 als PWM mit 50Hz
##p.start(2.5) # Initialisierung
#try:
#  while True:
#    GPIO.output(servoPIN, GPIO.LOW)
#    time.sleep(1)
#    GPIO.output(servoPIN, GPIO.HIGH)
#    time.sleep(0.1)
#except KeyboardInterrupt:
#  p.stop()
#  GPIO.cleanup()
  

import pigpio
from time import sleep

def is_stopped(pi):
    sleep(1)
    if pi.read(27) == 1:
        print('Button Pressed again (off)')
        pi.stop()
        return True
    else:
        return False
    
# connect to the 
pi = pigpio.pi()
pi.set_mode(27, pigpio.INPUT)
pi.set_pull_up_down(27, pigpio.PUD_UP)

while True:
    if pi.read(27) == 0:
        print('Button Pressed (on)')
        sleep(2)
        break

# loop forever
try:
    while True:
        pi.set_servo_pulsewidth(18, 0)    # off
        if is_stopped(pi):
            break
        pi.set_servo_pulsewidth(18, 670) # position anti-clockwise
        if is_stopped(pi):
            break
        pi.set_servo_pulsewidth(18, 1500) # middle
        if is_stopped(pi):
            break
        pi.set_servo_pulsewidth(18, 2330) # position clockwise
        if is_stopped(pi):
            break
except KeyboardInterrupt:
    pi.set_servo_pulsewidth(18, 0)    # off
    sleep(1)
    pi.stop()