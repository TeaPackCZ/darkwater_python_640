import time
from darkwater_640.darkwater_640 import dw_Controller, dw_Servo, dw_Motor

dw = dw_Controller( addr=0x60 )
m1 = dw.getMotor(1)
m2 = dw.getMotor(2)
m3 = dw.getMotor(3)
m4 = dw.getMotor(4)
m5 = dw.getMotor(5)
m6 = dw.getMotor(6)

m1.setMotorSpeed(0)
time.sleep(1)

##time.sleep(10)
print "Set forward"
m1.setMotorSpeed(255)
time.sleep(1)
print "stop"
m1.setMotorSpeed(0)
time.sleep(1)
print "Set reverse"
m1.setMotorSpeed(-255)
time.sleep(1)
print "stop"
m1.setMotorSpeed(0)
