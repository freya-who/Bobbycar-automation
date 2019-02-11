from gpiozero import Servo, LED

# https://www.raspberrypi-spy.co.uk/2018/02/basic-servo-use-with-the-raspberry-pi/ 

SERVOPIN = 18
ACCPIN = 17

##dummyservo
#class Servo:
#    def __init__(self, num):
#        self.pin = num
#        self.value = 0
#        
#class LED:
#    def __init__(self, num):
#        self.pin = num
#        self.state = False
#    def on(self):
#        self.state = True
#        print('LED on')
#    def off(self):
#        self.state = False
#        print('LED off')

class BobbycarDriver:
    def __init__(self):
        self.steeringwheelPos = 0
        self.servo = Servo(SERVOPIN)
        self.accelerator = LED(ACCPIN) 
        
    def driveLeft(self, amount):
        if 0 <= amount <= 1:
            self.servo.value = -amount
            print('servo links gelenkt %s' % - amount)
        else:
            print('Parameter amount must be between 0 and 1')
            
    def driveStraight(self):
        self.servo.value = 0
    
    def driveRight(self, amount):
        if 0 <= amount <= 1:
            self.servo.value = amount
            print('servo rechts gelenkt %s' % amount)
        else:
            print('Parameter amount must be between 0 and 1')
        
    def accelerate(self):
        self.accelerator.on()
        
    def stop(self):
        self.accelerator.off()
        
    
        
        