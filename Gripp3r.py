#!/usr/bin/env python3

# -----------------------------------------------------------------------------
# This code is modified from 
# https://sites.google.com/site/ev3python/learn_ev3_python/remote-control
# The copyright for the original code is held by
# Denis Demidov <dennis.demidov@gmail.com>
# -----------------------------------------------------------------------------

from time import sleep
from ev3dev.ev3 import *

rMotor = LargeMotor('outC')
lMotor = LargeMotor('outB')
assert rMotor.connected
assert lMotor.connected
primarySpeed = 750.0

gripMotor = MediumMotor('outA')
assert gripMotor.connected
gripSpeed = 250.0

rcDriveChan = RemoteControl(channel=1)
assert rcDriveChan.connected

rcGripChan = RemoteControl(channel=2)
assert rcGripChan.connected

bugleBaseTone = 440
bugleTune = [(bugleBaseTone, 250, 250), (bugleBaseTone, 250, 250),
    (bugleBaseTone, 250, 250), (2*bugleBaseTone, 750, 0)]
closingTune = [(bugleBaseTone, 250, 250), (bugleBaseTone/2, 500, 0)]

#############################
# program begins
#############################

# sound the charge
Sound.tone(bugleTune).wait()

# Turn leds off
Leds.all_off()

def roll(motor, led_group, direction):
    """
    Generate remote control event handler for channel 1 signals. These control 
    locomotion of the Gripp3r robot.  
    
    It rolls given motor into given direction (1 for forward, -1 for backward). 
    When motor rolls forward, the given led group flashes green, when backward 
    -- red. When motor stops, the leds are turned off.

    The on_press function has signature required by RemoteControl class.
    It takes boolean state parameter; True when button is pressed, False
    otherwise.
    """
    def on_press(state):
        if state:
            # Roll when button is pressed
            motor.run_forever(speed_sp=primarySpeed*direction)
            Leds.set_color(led_group, direction > 0 and Leds.GREEN or Leds.RED)
        else:
            # Stop otherwise
            motor.stop(stop_action='brake')
            Leds.set(led_group, brightness_pct=0)

    return on_press

# Assign event handler to each of the remote buttons on channel 1
rcDriveChan.on_red_up    = roll(lMotor, Leds.LEFT,   1)
rcDriveChan.on_red_down  = roll(lMotor, Leds.LEFT,  -1)
rcDriveChan.on_blue_up   = roll(rMotor, Leds.RIGHT,  1)
rcDriveChan.on_blue_down = roll(rMotor, Leds.RIGHT, -1)

def grab(motor, led_group, direction):
    """
    Generate remote control event handler for channel 2 remote control 
    signals.   

    The on_press function has signature required by RemoteControl class.
    It takes boolean state parameter; True when button is pressed, False
    otherwise.
    """
    def on_press(state):
        if state:
            # Grab when button is pressed
            motor.run_forever(speed_sp=gripSpeed*direction)
            Leds.set_color(led_group, direction > 0 and Leds.GREEN or Leds.RED)
        else:
            # Otherwise stop
            motor.stop(stop_action='brake')
            Leds.set(led_group, brightness_pct=0)
    
    return on_press

#Assign event handler to each of the remote buttons on channel 2
rcGripChan.on_blue_up   = grab(gripMotor, Leds.RIGHT, 1)
rcGripChan.on_blue_down = grab(gripMotor, Leds.RIGHT, -1)

# Enter event processing loop
#while not button.any():   #not working so commented out
while True:   #replaces previous line so use Ctrl-C to exit
    rcDriveChan.process()
    rcGripChan.process()
    sleep(0.01)

# Press Ctrl-C to exit

# Sound.tone(closingTune).wait()
