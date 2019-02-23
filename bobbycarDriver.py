import pigpio
from time import sleep

SERVOPIN = 18
ACCPIN = 17

class BobbycarDriver:
    def __init__(self):
        self.pi = pigpio.pi()
        self.pi.set_mode(SERVOPIN, pigpio.OUTPUT)
        self.pi.set_mode(ACCPIN, pigpio.OUTPUT)
        self.steeringwheelPos = 0
        self.currentSteeringDirection = "straight"

    def driveLeft(self, amount):
        if 0 <= amount <= 1:
            # map 0...1 to 1500...1000
            servoAmount = 1500 - 500*amount
            self.pi.set_servo_pulsewidth(SERVOPIN, servoAmount)
            print('servo steered left by %s' % amount)
            self.currentSteeringDirection = "left"
        else:
            print('Parameter amount must be between 0 and 1')
            
    def driveStraight(self):
        self.pi.set_servo_pulsewidth(SERVOPIN, 1500)
        self.currentSteeringDirection = "straight"
    
    def driveRight(self, amount):
        if 0 <= amount <= 1:
            # map 0...1 to 1500...2000
            servoAmount = 1500 + 500*amount
            self.pi.set_servo_pulsewidth(SERVOPIN, servoAmount)
            print('servo steered right by %s' % amount)
            self.currentSteeringDirection = "right"
        else:
            print('Parameter amount must be between 0 and 1')
        
    def accelerate(self):
        self.pi.write(ACCPIN,1)
#        
#        # maybe use some software PWM (1000 Hz maybe?)
#        self.pi.set_PWM_frequency(ACCPIN,1000)
#        # map 0...1 to 0...255 for dutycycle
#        dutyCycle = amount * 255
#        self.pi.set_PWM_dutycycle(ACCPIN, dutyCycle)
               
    def stop(self):
        self.pi.write(ACCPIN,0)
    
    def cleanup(self):
        self.pi.stop()