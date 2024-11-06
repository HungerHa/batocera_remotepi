#!/usr/bin/env python3
# Created on: 2024-11-03 13:56
# Changed on: 2024-11-03 16:56
# Author: HarryH
# Version: 1.0.0
#
# Changelog:
# 1.0.0 2024-11-03
# - initial version with python3

import os
import time
os.environ['LG_WD'] = '/tmp'

from gpiozero import LED, Button
from subprocess import check_call

# this is the GPIO pin receiving the shut-down signal
SHUTDOWN_PIN=14 # GPIO14/PIN 8

power_btn_triggered = False


def power_btn_pressed(chip=None, gpio=None, level=None, timestamp=None):
    global power_btn_triggered
    power_btn_triggered = True


def shutdown():
    check_call(['poweroff'])


# set GPIO14 to input
btn = Button(SHUTDOWN_PIN, pull_up=False)
btn.when_pressed = power_btn_pressed

while True:
    time.sleep(1.0)
    # check if GPIO14 is going to high
    if power_btn_triggered:
        power_btn_triggered = False
        # change GPIO14 to output and set it to high level
        btn.close()
        led = LED(SHUTDOWN_PIN)
        led.on
        time.sleep(3.0)
        shutdown()
        break
