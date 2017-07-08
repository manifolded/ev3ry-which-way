#!/usr/bin/env python3

from time import sleep
from ev3dev.ev3 import *

lMotor = LargeMotor('outC')
rMotor = LargeMotor('outB')
primarySpeed = 500

bugleBaseTone = 440
bugleTune = [(bugleBaseTone, 250, 250), (bugleBaseTone, 250, 250), (bugleBaseTone, 250, 250),
             (2*bugleBaseTone, 750, 0)]

touch = TouchSensor('in2')
assert touch.connected, "Connect a touch sensor to sensor port 2"

def goForward():
    lMotor.run_forever(speed_sp=primarySpeed)
    rMotor.run_forever(speed_sp=primarySpeed)
    return

def allStop():
    lMotor.stop(stop_action="hold")
    rMotor.stop(stop_action="hold")
    return

#############################
# program start
#
# sound the charge
Sound.tone(bugleTune).wait()

while not touch.value():
    goForward()
allStop()
