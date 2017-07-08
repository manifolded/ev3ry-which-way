#!/usr/bin/env python3

from time import sleep
from ev3dev.ev3 import *

lMotor = LargeMotor('outC')
rMotor = LargeMotor('outB')
primarySpeed = 750.0

bugleBaseTone = 440
bugleTune = [(bugleBaseTone, 250, 250), (bugleBaseTone, 250, 250), (bugleBaseTone, 250, 250),
             (2*bugleBaseTone, 750, 0)]

closingTune = [(bugleBaseTone, 250, 250), (bugleBaseTone/2, 500, 0)]

touch = TouchSensor('in2')
assert touch.connected, "Connect a touch sensor to sensor port 2"
gyro = GyroSensor('in3')
assert gyro.connected, "Connect a gyro sensor to sensor port 3"
# The gyro measures in degrees and increases in the clockwise direction.
# It is very sensitive to its initial orientation.  Make sure to have its z-axis aligned on 
# startup of the code.
gyro.mode = 'GYRO-ANG'

def clamp(n, floor, ceiling):
    return max(floor, min(ceiling, n))

def diffDrive(forward, turn):
    lMotor.run_forever(speed_sp=clamp(forward + turn, -1000, 1000))
    rMotor.run_forever(speed_sp=clamp(forward - turn, -1000, 1000))
    return

def allStop():
    lMotor.stop(stop_action="hold")
    rMotor.stop(stop_action="hold")
    return

def fixHeading(speed, heading, multiplier):
    turnVal = clamp(-1.0 * multiplier * (gyro.value() - heading), -500, 500)
    diffDrive(speed, turnVal)
    return

#############################
# program start
#
# sound the charge
Sound.tone(bugleTune).wait()

tgtHeading = gyro.value()
while not touch.value():
    fixHeading(primarySpeed, tgtHeading, 20.0)

allStop()
Sound.tone(closingTune).wait()