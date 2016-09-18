#!/usr/bin/python

import RPi.GPIO as GPIO
from PCA9685 import PCA9685
import time
import math

# Stepper motor code based on Adafruit Python Library for DC + Stepper Motor HAT
# Written by Limor Fried for Adafruit Industries. MIT license.

class dw_Stepper:
        MICROSTEPS = 8
        MICROSTEP_CURVE = [0, 50, 98, 142, 180, 212, 236, 250, 255]

        #MICROSTEPS = 16
        # a sinusoidal curve NOT LINEAR!
        #MICROSTEP_CURVE = [0, 25, 50, 74, 98, 120, 141, 162, 180, 197, 212, 225, 236, 244, 250, 253, 255]

        def __init__(self, controller, num, steps=200, forcemode=False):
                self.speed = 0
                self.MC = controller
                self.motornum = num
                modepin = in1 = in2 = 0

                self.revsteps = steps
                self.sec_per_step = 0.1
                self.steppingcounter = 0
                self.currentstep = 0

                if(self.MC.getMode() != dw_Controller.ININ and forcemode != True ):
                        raise NameError('Mode needs to be set to ININ for stepper mode operation')
                else:
                        self.MC.setMode(dw_Controller.ININ)

                if (num == 0):
                        ain1 = 2 
                        ain2 = 3  
                        bin1 = 4  
                        bin2 = 5  
                elif (num == 1):
                        ain1 = 6  
                        ain2 = 7  
                        bin1 = 8  
                        bin2 = 9  
                elif (num == 2):
                        ain1 = 10  
                        ain2 = 11  
                        bin1 = 12  
                        bin2 = 13  
                else:
                        raise NameError('Stepper must be between 1 and 3 inclusive')

                self.ain1 = ain1
                self.ain2 = ain2
                self.bin1 = bin1
                self.bin2 = bin2

                # switch off both drivers
                self.run(dw_Controller.STOP, 0)

        def run(self, command, speed = 0):
                if not self.MC:
                        return
                
                if (command == dw_Controller.STOP):
                        self.MC.setPin(self.ain1, 1)
                        self.MC.setPin(self.ain2, 1)
                        self.MC.setPin(self.bin1, 1)
                        self.MC.setPin(self.bin2, 1)

        def off(self):
                self.run(dw_Controller.STOP, 0)

        def setSpeed(self, rpm):
                self.sec_per_step = 60.0 / (self.revsteps * rpm)
                self.steppingcounter = 0

        def oneStep(self, dir, style):
                pwm_a = pwm_b = 255

                # first determine what sort of stepping procedure we're up to
                if (style == dw_Controller.SINGLE):
                        if ((self.currentstep/(self.MICROSTEPS/2)) % 2):
                                # we're at an odd step, weird
                                if (dir == dw_Controller.FORWARD):
                                        self.currentstep += self.MICROSTEPS/2
                                else:
                                        self.currentstep -= self.MICROSTEPS/2
                        else:
                                # go to next even step
                                if (dir == dw_Controller.FORWARD):
                                        self.currentstep += self.MICROSTEPS
                                else:
                                        self.currentstep -= self.MICROSTEPS
                if (style == dw_Controller.DOUBLE):
                        if not (self.currentstep/(self.MICROSTEPS/2) % 2):
                                # we're at an even step, weird
                                if (dir == dw_Controller.FORWARD):
                                        self.currentstep += self.MICROSTEPS/2
                                else:
                                        self.currentstep -= self.MICROSTEPS/2
                        else:
                                # go to next odd step
                                if (dir == dw_Controller.FORWARD):
                                        self.currentstep += self.MICROSTEPS
                                else:
                                        self.currentstep -= self.MICROSTEPS

                if (style == dw_Controller.MICROSTEP):
                        if (dir == dw_Controller.FORWARD):
                                self.currentstep += 1
                        else:
                                self.currentstep -= 1

                        # go to next 'step' and wrap around
                        self.currentstep += self.MICROSTEPS * 4
                        self.currentstep %= self.MICROSTEPS * 4

                        pwm_a = pwm_b = 0
                        if (self.currentstep >= 0) and (self.currentstep < self.MICROSTEPS):
                                pwm_a = self.MICROSTEP_CURVE[self.MICROSTEPS - self.currentstep]
                                pwm_b = self.MICROSTEP_CURVE[self.currentstep]
                        elif (self.currentstep >= self.MICROSTEPS) and (self.currentstep < self.MICROSTEPS*2):
                                pwm_a = self.MICROSTEP_CURVE[self.currentstep - self.MICROSTEPS]
                                pwm_b = self.MICROSTEP_CURVE[self.MICROSTEPS*2 - self.currentstep]
                        elif (self.currentstep >= self.MICROSTEPS*2) and (self.currentstep < self.MICROSTEPS*3):
                                pwm_a = self.MICROSTEP_CURVE[self.MICROSTEPS*3 - self.currentstep]
                                pwm_b = self.MICROSTEP_CURVE[self.currentstep - self.MICROSTEPS*2]
                        elif (self.currentstep >= self.MICROSTEPS*3) and (self.currentstep < self.MICROSTEPS*4):
                                pwm_a = self.MICROSTEP_CURVE[self.currentstep - self.MICROSTEPS*3]
                                pwm_b = self.MICROSTEP_CURVE[self.MICROSTEPS*4 - self.currentstep]


                # go to next 'step' and wrap around
                self.currentstep += self.MICROSTEPS * 4
                self.currentstep %= self.MICROSTEPS * 4

                # set up coil energizing!
                coils = [0, 0, 0, 0]

                if (style == dw_Controller.MICROSTEP):
                        if (self.currentstep >= 0) and (self.currentstep < self.MICROSTEPS):
                                coils = [1, 1, 0, 0]
                        elif (self.currentstep >= self.MICROSTEPS) and (self.currentstep < self.MICROSTEPS*2):
                                coils = [0, 1, 1, 0]
                        elif (self.currentstep >= self.MICROSTEPS*2) and (self.currentstep < self.MICROSTEPS*3):
                                coils = [0, 0, 1, 1]
                        elif (self.currentstep >= self.MICROSTEPS*3) and (self.currentstep < self.MICROSTEPS*4):
                                coils = [1, 0, 0, 1]
                else:
                        step2coils = [  [1, 0, 0, 0],
                                        [1, 1, 0, 0],
                                        [0, 1, 0, 0],
                                        [0, 1, 1, 0],
                                        [0, 0, 1, 0],
                                        [0, 0, 1, 1],
                                        [0, 0, 0, 1],
                                        [1, 0, 0, 1] ]
                        coils = step2coils[self.currentstep/(self.MICROSTEPS/2)]

                self.MC.setPin(self.ain1, coils[0]) #ain2
                self.MC.setPin(self.bin1, coils[1]) #bin1
                self.MC.setPin(self.ain2, coils[2]) #ain1
                self.MC.setPin(self.bin2, coils[3]) #bin2

                return self.currentstep

        def step(self, steps, direction, stepstyle):
              s_per_s = self.sec_per_step
              lateststep = 0

              if (stepstyle == dw_Controller.MICROSTEP):
                      s_per_s /= self.MICROSTEPS
                      steps *= self.MICROSTEPS

              for s in range(steps):
                      lateststep = self.oneStep(direction, stepstyle)
                      time.sleep(s_per_s)

              if (stepstyle == dw_Controller.MICROSTEP):
                      # this is an edge case, if we are in between full steps, lets just keep going
                      # so we end on a full step
                      while (lateststep != 0) and (lateststep != self.MICROSTEPS):
                              lateststep = self.oneStep(dir, stepstyle)
                              time.sleep(s_per_s)

class dw_Motor:
        def __init__(self, controller, num):
                self.speed = 0
                self.MC = controller
                self.motornum = num
                modepin = in1 = in2 = 0

                if (num == 0):
                         in2 = 2   #phase
                         in1 = 3   #enable
                elif (num == 1):
                         in2 = 4   #phase
                         in1 = 5   #enable
                elif (num == 2):
                         in2 = 6  #phase
                         in1 = 7  #enable
                elif (num == 3):
                         in2 = 8  #phase
                         in1 = 9  #enable
                elif (num == 4):
                         in2 = 10   #phase
                         in1 = 11   #enable
                elif (num == 5):
                         in2 = 12  #phase
                         in1 = 13  #enable
                else:
                        raise NameError('Motors must be between 1 and 6 inclusive')

                # for phase enable
                self.PHpin = in2
                self.ENpin = in1
                # for in/in
                self.IN2pin = in2
                self.IN1pin = in1
                # switch off
                self.run(dw_Controller.STOP, 0)

        def setMotorSpeed(self, value):
                # Check for PWM values
                if(value > 1000) and (value < 1500):
                        self.run(dw_Controller.REVERSE, round(translate(value,1500,1000, 0, 255)))
                if(value > 1500) and (value <= 2000):
                        self.run(dw_Controller.FORWARD, round(translate(value, 1500, 2000, 0, 255)))
                if(value == 1500):
                        self.run(dw_Controller.STOP, 0)
                if(value > 0) and (value <= 255):
                        self.run(dw_Controller.FORWARD, value)
                if(value == 0):
                        self.run(dw_Controller.STOP, value)
                if(value < 0) and (value >= -255):
                        self.run(dw_Controller.REVERSE, abs(value))

        def run(self, command, speed = 0):
                if not self.MC:
                        return
                if (self.MC.getMode() == dw_Controller.PHASE):
                        if (command == dw_Controller.FORWARD):
                                self.MC.setPin(self.PHpin, 0)
                                self.MC._pwm.set_pwm(self.ENpin, 0, speed*16)
                        if (command == dw_Controller.REVERSE):
                                self.MC.setPin(self.PHpin, 1)
                                self.MC._pwm.set_pwm(self.ENpin, 0, speed*16)
                        if (command == dw_Controller.STOP):
                                self.MC.setPin(self.PHpin, 0)
                                self.MC.setPin(self.ENpin, 0)
                else:   ## IN/IN mode
                        if (command == dw_Controller.FORWARD):
                                self.MC.setPin(self.IN2pin, 0)
                                self.MC._pwm.set_pwm(self.IN1pin, 0, speed*16)
                        if (command == dw_Controller.REVERSE):
                                self.MC.setPin(self.IN1pin, 0)
                                self.MC._pwm.set_pwm(self.IN2pin, 0, speed*16)
                        if (command == dw_Controller.STOP):
                                self.MC.setPin(self.IN1pin, 1)
                                self.MC.setPin(self.IN2pin, 1)
                        if (command == dw_Controller.COAST):
                                self.MC.setPin(self.IN1pin, 0)
                                self.MC.setPin(self.IN2pin, 0)   

        def off(self):
                self.run(dw_Controller.STOP, 0)


class dw_Servo:
        def __init__(self, controller, num, freq):

                _SERVO_MIN_MS = 1.250 #ms
                _SERVO_MAX_MS = 1.750 #ms

                self.speed = 0
                self.MC = controller
                self.cnum = num
                self.pin = 0

                self.freq = freq

                self.servo_min = math.trunc( ( _SERVO_MIN_MS * 4096 ) / (1000.0 / self.freq ) - 1 )
                self.servo_max = math.trunc( ( _SERVO_MAX_MS * 4096 ) / (1000.0 / self.freq ) - 1 )

                self.servo_zero = math.trunc( ( self.servo_min + self.servo_max ) / 2 ) # halfway = 0 degrees


                if (num == 0):
                    self.pin = 0
                elif (num == 1):
                    self.pin = 1
                else:
                    raise NameError('Port must be between 0 and 1 inclusive')

                # switch off
                self.off()

        def off(self):
                self.MC.setPin(self.pin, 0)

        def setAngle(self, angle):
                pulse = self.servo_zero + ( (self.servo_zero - self.servo_min ) * angle / 80 )
                print "angle=%s pulse=%s" % (angle, pulse)
                #self.setPWMmS( pulse )

        def setPWM(self, value):
                if(value > 0):
                    self.MC._pwm.set_pwm(self.pin, 0, int(value) )
                if(value == 0):
                    self.off()

        def setPWMmS(self, length_ms):
                self.setPWM( math.trunc( ( length_ms * 4096 ) / ( 1000.0 / self.freq ) ) - 1 )

        def setPWMuS(self, length_us):
                self.setPWM( math.trunc( ( length_us * 4096 ) / ( 1000000.0 / self.freq ) ) -1 )



class dw_Controller:
        FORWARD = 1
        REVERSE = 2
        BRAKEFORWARD = 3
        BRAKEREVERSE = 4
        STOP = 5 #brake
        COAST = 6 # in/in only

        SINGLE = 1
        DOUBLE = 2
        INTERLEAVE = 3
        MICROSTEP = 4

        ININ = 0
        PHASE = 1

        def __init__(self, addr = 0x60, freq = 100, correctionFactor = 1.0):
                self._i2caddr = addr            # default addr on HAT
                self._frequency = freq          # default @1600Hz PWM freq
                # self.steppers = [ Adafruit_StepperMotor(self, 1), Adafruit_StepperMotor(self, 2) ]
                self._pwm =  PCA9685(addr)
                self._pwm.set_pwm_freq(self._frequency, correctionFactor)
                # Just gonna default to high for now
                GPIO.setmode(GPIO.BCM)
                GPIO.setwarnings(False)
                GPIO.setup(27, GPIO.OUT)

                self.setMode(self.ININ) # set high for en/phase mode - low = in/in mode

                self.motors = [ dw_Motor(self, m) for m in range(6) ]
                self.servos = [ dw_Servo(self, m, freq) for m in range(2) ]

                self.steppers =  [ dw_Stepper(self, m) for m in range(3) ]

        def setMode(self, mode = 1):
                if (mode == self.ININ):
                        self._mode = self.ININ
                        GPIO.output(27, GPIO.LOW)
                else:
                        self._mode = self.PHASE
                        GPIO.output(27, GPIO.HIGH)

        def getMode(self):
                return self._mode

        def setPin(self, pin, value):
                if (pin < 0) or (pin > 15):
                        raise NameError('PWM pin must be between 0 and 15 inclusive')
                if (value != 0) and (value != 1):
                        raise NameError('Pin value must be 0 or 1!')
                if (value == 0):
                        self._pwm.set_pwm(pin, 0, 4096)
                if (value == 1):
                        self._pwm.set_pwm(pin, 4096, 0)

        def setAllPin(self, value):
                if (pin < 0) or (pin > 15):
                        raise NameError('PWM pin must be between 0 and 15 inclusive')
                if (value != 0) and (value != 1):
                        raise NameError('Pin value must be 0 or 1!')
                if (value == 0):
                        self._pwm.set_all_pwm(0, 4096)
                if (value == 1):
                        self._pwm.set_all_pwm(4096, 0)

        def getMotor(self, num):
                if (num < 1) or (num > 6):
                        raise NameError('Motors must be between 1 and 6 inclusive')
                return self.motors[num-1]

        def getServo(self, num):
                if (num < 1) or (num > 2):
                        raise NameError('Servos must be between 1 and 2 inclusive')
                return self.servos[num-1]

        def getStepper(self, num):
                if (num < 1) or (num > 3):
                        raise NameError('Stepper motors must be between 1 and 3 inclusive')
                return self.steppers[num-1]

        def setAllPWM(self, value):
                if(value > 0):
                        self._pwm.set_all_pwm(0, value)
                if(value == 0):
                        self.allOff()

        def setAllPWMmS(self, value):
                if(value > 0):
                        self._pwm.set_all_pwm(0, value)
                if(value == 0):
                        self.allOff()

        def setAllPWMuS(self, value):
                if(value > 0):
                        self._pwm.set_all_pwm(0, value)
                if(value == 0):
                        self.allOff()

        def allOff(self):
                this.setAllPin( 0 );

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)