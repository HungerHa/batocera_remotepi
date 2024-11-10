#!/usr/bin/env python3
# Created on: 2024-11-03 13:56
# Changed on: 2024-11-09 21:03
# Author: HarryH
# Version: 1.0.3
#
# Changelog:
# 1.0.3 2024-11-09
# - added gpiod 1.5.4 (unofficial) support for RPi4/5
# 1.0.2 2024-11-05
# - suppress RPi.GPIO warnings
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
gpiod_spec = importlib.util.find_spec('gpiod')

if gpiod_spec is not None:
    import gpiod
elif rpigpio_spec is not None:
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


if gpiod_spec is not None:
    # test for gpiochip numbering
    try:
        # temporary RPi5 gpiochip assignment up to kernel 6.6.45
        # https://github.com/raspberrypi/linux/pull/6144
        chip = gpiod.chip('gpiochip4')
    except Exception as gpioerr:
        # common
        chip = gpiod.chip('gpiochip0')

    shutdown_pin=chip.get_line(SHUTDOWN_PIN)
    shutdown_config = gpiod.line_request()
    shutdown_config.consumer = "remotepi"

    try:
        # set GPIO14 to input
        shutdown_config.request_type = gpiod.line_request.DIRECTION_INPUT
        shutdown_config.flags = gpiod.line_request.FLAG_BIAS_PULL_DOWN
        shutdown_pin.request(shutdown_config)
        # check if GPIO14 is going to high
        while shutdown_pin.get_value() == 0:
            time.sleep(1.0)
        # change GPIO14 to output and set it to high level
        shutdown_pin.set_config(direction=gpiod.line_request.DIRECTION_OUTPUT, flags=gpiod.line_request.FLAG_BIAS_DISABLE)
        shutdown_pin.set_value(1)
        time.sleep(3.0)
    finally:
        shutdown_pin.release()
    shutdown()


elif rpigpio_spec is not None:
    # set GPIO14 to input
    GPIO.setwarnings(False)
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
