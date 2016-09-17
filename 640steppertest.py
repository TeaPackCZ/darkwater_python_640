import time
from darkwater_640.darkwater_640 import dw_Controller, dw_Servo, dw_Motor

dw = dw_Controller( addr=0x60 )
s1 = dw.getStepper(1)
m3 = dw.getMotor(3)

s1.off()
m3.off()
time.sleep(1)

m3.setMotorSpeed(-255)
s1.oneStep( dw_Controller.FORWARD, dw_Controller.SINGLE);

s1.off()
m3.off()