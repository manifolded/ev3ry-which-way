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
headingEpsilon = 1.0
ir = InfraredSensor('in1')
assert ir.connected, "Connect an infrared sensor to sensor port 1"
ir.mode = 'IR-PROX'

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

def fixHeading(speed, currentHeading, targetHeading, multiplier):
    # Applies a linear first order feedback (with amplitude limiting) to the steering
    # to bring the current heading to align with the target heading over time.  It 
    # "fixes" the heading in the sense of fixing a point on the horizon and steering
    # for it.
    turnVal = clamp(-1.0 * multiplier * (currentHeading - targetHeading), -500, 500)
    diffDrive(speed, turnVal)
    return

def modAdd(augend, addend):
    augend += addend + 720
    augend %= 360
    return augend

#############################
# program begins
#############################

# sound the charge
Sound.tone(bugleTune).wait()

tgtHeading = gyro.value()
turning = False

while not touch.value():

    proxObsticleQ = ir.value() < 60.0
    currHeading = gyro.value()

    ######################################################
    # state machine
    ######################################################

    # state 1 - TURN from detected obstacle
    if turning:
        fixHeading(0.0, currHeading, tgtHeading, 20.0)

        # state exit criterion
        if abs(currHeading - tgtHeading) < headingEpsilon:
            turning = False

    # state 2 - DRIVE until obstacle detected
    else:
        fixHeading(primarySpeed, currHeading, tgtHeading, 20.0)

        # state exit criterion
        if proxObsticleQ:
            # turn left 120 deg
            tgtHeading = modAdd(tgtHeading, -120.0)
            turning = True

allStop()
Sound.tone(closingTune).wait()