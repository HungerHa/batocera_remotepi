#!/usr/bin/env python3
# Created on: 2024-11-03 15:30
# Changed on: 2024-11-04 19:58
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
import time
os.environ['LG_WD'] = '/tmp'
rpigpio_spec = importlib.util.find_spec('RPi.GPIO')
if rpigpio_spec is not None:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
else:
    from gpiozero import LED

# these are the GPIO pins to communicate the shut-down signal to the RemotePi hardware
SHUTDOWN_PIN=14 # GPIO14/PIN 8/UART0 TXD
COMM_PIN=15 # GPIO15/PIN 10/UART0 RXD


def initiate_hw_shutdown_gpiozero():
    # execute shutdown sequence on pin
    # set GPIO15 to output and high level for 125ms
    comm_pin = LED(COMM_PIN)
    comm_pin.on
    time.sleep(0.125)
    # change the output to low level for 200ms
    comm_pin.off
    time.sleep(0.2)
    # change the output to high level for 400ms
    comm_pin.on
    time.sleep(0.4)
    # change the output to low level
    comm_pin.off
    # set GPIO 14 high to feedback shutdown to RemotePi Board
    # because the irswitch.sh has already been terminated
    shutdown_pin = LED(SHUTDOWN_PIN)
    shutdown_pin.on
    time.sleep(4)


def initiate_hw_shutdown():
    GPIO.setwarnings(False)
    # execute shutdown sequence on pin
    # set GPIO15 to output and high level for 125ms
    GPIO.setup(COMM_PIN, GPIO.OUT)
    GPIO.output(COMM_PIN, True)
    time.sleep(0.125)
    # change the output to low level for 200ms
    GPIO.output(COMM_PIN, False)
    time.sleep(0.2)
    # change the output to high level for 400ms
    GPIO.output(COMM_PIN, True)
    time.sleep(0.4)
    # change the output to low level
    GPIO.output(COMM_PIN, False)
    # set GPIO 14 high to feedback shutdown to RemotePi Board
    # because the irswitch.sh has already been terminated
    GPIO.setup(SHUTDOWN_PIN, GPIO.OUT)
    GPIO.output(SHUTDOWN_PIN, True)
    time.sleep(4)
    GPIO.cleanup()


if rpigpio_spec is not None:
    initiate_hw_shutdown()
else:
    initiate_hw_shutdown_gpiozero()
