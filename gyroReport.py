#!/usr/bin/env python3

from time import sleep
from ev3dev.ev3 import *

lMotor = LargeMotor('outC')
rMotor = LargeMotor('outB')
primarySpeed = 0

bugleBaseTone = 440
bugleTune = [(bugleBaseTone, 250, 250), (bugleBaseTone, 250, 250), (bugleBaseTone, 250, 250),
             (2*bugleBaseTone, 750, 0)]

touch = TouchSensor('in2')
assert touch.connected, "Connect a touch sensor to sensor port 2"
gyro = GyroSensor('in3')
assert gyro.connected, "Connect a gyro sensor to sensor port 3"
# The gyro measures in degrees and increases in the clockwise direction.
# It is very sensitive to its initial orientation.  Make sure to have its z-axis aligned on 
# startup of the code.
gyro.mode = 'GYRO-ANG'

def diffDrive(forward, turn):
    lMotor.run_forever(speed_sp = forward + turn)
    rMotor.run_forever(speed_sp = forward - turn)
    return

def allStop():
    lMotor.stop(stop_action="hold")
    rMotor.stop(stop_action="hold")
    return

def reportGyroAngle():
    units = gyro.units # reports 'deg' meaning degrees
    theta = gyro.value()
    print(str(theta) + " " + units)
    return theta

#############################
# program start
#
# sound the charge
Sound.tone(bugleTune).wait()

while not touch.value():
    Sound.tone(1000+reportGyroAngle()*10, 40).wait()    
allStop()
Sound.beep()
