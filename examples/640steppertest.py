import time
from darkwater_640 import dw_Controller, dw_Stepper

dw = dw_Controller( addr=0x60 )
s1 = dw.getStepper(1)
s2 = dw.getStepper(2)
s3 = dw.getStepper(3)

s1.off()
s2.off()
s3.off()

s1.setMotorSpeed(200)
s2.setMotorSpeed(200)
s3.setMotorSpeed(200)

s1.step( 400, dw_Controller.FORWARD, dw_Controller.DOUBLE )
s2.step( 400, dw_Controller.FORWARD, dw_Controller.DOUBLE )
s3.step( 400, dw_Controller.FORWARD, dw_Controller.DOUBLE )

s1.step( 400, dw_Controller.REVERSE, dw_Controller.DOUBLE )
s2.step( 400, dw_Controller.REVERSE, dw_Controller.DOUBLE )
s3.step( 400, dw_Controller.REVERSE, dw_Controller.DOUBLE )

s1.step( 400, dw_Controller.FORWARD, dw_Controller.DOUBLE )
s2.step( 400, dw_Controller.FORWARD, dw_Controller.DOUBLE )
s3.step( 400, dw_Controller.FORWARD, dw_Controller.DOUBLE )

s1.step( 400, dw_Controller.REVERSE, dw_Controller.DOUBLE )
s2.step( 400, dw_Controller.REVERSE, dw_Controller.DOUBLE )
s3.step( 400, dw_Controller.REVERSE, dw_Controller.DOUBLE )

s1.off()
s2.off()
s3.off()