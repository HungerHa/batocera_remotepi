#!/usr/bin/env python3
# Created on: 2024-11-03 13:56
# Changed on: 2024-11-04 19:52
# Author: HarryH
# Version: 1.0.1
#
# Changelog:
# 1.0.1 2024-11-04
# - added RPi.GPIO support
# 1.0.0 2024-11-03
# - initial version with python3

import importlib.util
import os
from subprocess import check_call
import time
os.environ['LG_WD'] = '/tmp'
rpigpio_spec = importlib.util.find_spec('RPi.GPIO')
if rpigpio_spec is not None:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
else:
    # Only for kernel versions below 6.5.7
    # or if lgpio is available
    # because otherwise the edge detection will fail
    from gpiozero import LED, Button

# this is the GPIO pin receiving the shut-down signal
SHUTDOWN_PIN=14 # GPIO14/PIN 8

power_btn_triggered = False


def power_btn_pressed(chip=None, gpio=None, level=None, timestamp=None):
    global power_btn_triggered
    power_btn_triggered = True


def shutdown():
    check_call(['poweroff'])


if rpigpio_spec is not None:
    # set GPIO14 to input
    GPIO.setup(SHUTDOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    # check if GPIO14 is going to high
    while GPIO.input(SHUTDOWN_PIN) == GPIO.LOW:
        time.sleep(1.0)
    # change GPIO14 to output and set it to high level
    GPIO.setup(SHUTDOWN_PIN, GPIO.OUT)
    GPIO.output(SHUTDOWN_PIN, True)
    time.sleep(3.0)
    # print('shutdown initiated')
    shutdown()
    GPIO.cleanup()
else:
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
            # print('shutdown initiated')
            shutdown()
            break
