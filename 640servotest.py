import time
from darkwater_640.darkwater_640 import dw_Controller, dw_Servo, dw_Motor

dw = dw_Controller( addr=0x60 )
s1 = dw.getServo(1)
s2 = dw.getServo(2)

s1.off()
s2.off()
time.sleep(1)

##time.sleep(10)
print "Set forward - "
print "Servo 1"
s1.setPWMmS(2000)
time.sleep(1)
# print "Servo 2"
# s2.setPWMmS(2000)
# time.sleep(1)
# print "Set neutral - "
# print "Servo 1"
# s1.setPWMmS(1500)
# time.sleep(1)
# print "Servo 2"
# s2.setPWMmS(1500)
# time.sleep(1)
# print "Set reverse - "
# print "Servo 1"
# s1.setPWMmS(1000)
# time.sleep(1)
# print "Servo 2"
# s2.setPWMmS(1000)
# time.sleep(1)
# print "All off"
# s1.off()
# s2.off()
