#!/usr/bin/env python3
# Created on: 2024-11-03 15:30
# Changed on: 2024-11-03 17:36
# Author: HarryH
# Version: 1.0.0
#
# Changelog:
# 1.0.0 2024-11-03
# - initial version with python3

import os
import time
os.environ['LG_WD'] = '/tmp'

from gpiozero import LED

# these are the GPIO pins to communicate the shut-down signal to the RemotePi hardware
SHUTDOWN_PIN=14 # GPIO14/PIN 8/UART0 TXD
COMM_PIN=15 # GPIO15/PIN 10/UART0 RXD


def initiate_hw_shutdown():
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


initiate_hw_shutdown()
