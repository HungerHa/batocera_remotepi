#!/usr/bin/env python3
# Created on: 2024-11-03 15:30
# Changed on: 2024-11-10 18:04
# Author: HarryH
# Version: 1.0.3
#
# Changelog:
# 1.0.3 2024-11-10
# - added gpio 2.2.0 support
# - fixed gpio 1.5.4 chip initialization
# 1.0.2 2024-11-09
# - added gpiod 1.5.4 (unofficial) support for RPi4/5
# 1.0.1 2024-11-04
# - added RPi.GPIO support
# 1.0.0 2024-11-03
# - initial version with python3

import importlib.util
import os
import time
os.environ['LG_WD'] = '/tmp'
rpi_spec = importlib.util.find_spec('RPi')
if rpi_spec is not None:
    rpigpio_spec = importlib.util.find_spec('RPi.GPIO')
gpiod_spec = importlib.util.find_spec('gpiod')

if gpiod_spec is not None:
    import gpiod
elif rpigpio_spec is not None:
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


def initiate_hw_shutdown_gpiod():
    if not hasattr(gpiod, "is_gpiochip_device"): # gpiod <= 1.5.4 unofficial Python bindings
        # test for gpiochip numbering
        try:
            # temporary RPi5 gpiochip assignment up to kernel 6.6.45
            # https://github.com/raspberrypi/linux/pull/6144
            chip = gpiod.chip('4')
        except Exception as gpioerr:
            # common
            chip = gpiod.chip('0')

        comm_pin=chip.get_line(COMM_PIN)
        shutdown_pin=chip.get_line(SHUTDOWN_PIN)
        comm_config = gpiod.line_request()
        comm_config.consumer = "remotepi"
        comm_config.request_type = gpiod.line_request.DIRECTION_OUTPUT
        shutdown_config = gpiod.line_request()
        shutdown_config.consumer = "remotepi"
        shutdown_config.request_type = gpiod.line_request.DIRECTION_OUTPUT

        comm_pin.request(comm_config)
        shutdown_pin.request(shutdown_config)

        try:
            # execute shutdown sequence on pin
            # set GPIO15 to output and high level for 125ms
            comm_pin.set_value(1)
            time.sleep(0.125)
            # change the output to low level for 200ms
            comm_pin.set_value(0)
            time.sleep(0.2)
            # change the output to high level for 400ms
            comm_pin.set_value(1)
            time.sleep(0.4)
            # change the output to low level
            comm_pin.set_value(0)
            # set GPIO 14 high to feedback shutdown to RemotePi Board
            # because the irswitch.sh has already been terminated
            shutdown_pin.set_value(1)
            time.sleep(4)
        finally:
            comm_pin.release()
            shutdown_pin.release()
    else: # libgpiod/gpiod >= 2.0.2 official Python bindings
        # test for gpiochip numbering
        if gpiod.is_gpiochip_device('/dev/gpiochip4'):
            # temporary RPi5 gpiochip assignment up to kernel 6.6.45
            # https://github.com/raspberrypi/linux/pull/6144
            chip = gpiod.Chip('/dev/gpiochip4')
        else:
            # common
            chip = gpiod.Chip('/dev/gpiochip0')

        try:
            # execute shutdown sequence on pin
            # set GPIO15 to output and high level for 125ms
            comm_config_out = {COMM_PIN: gpiod.LineSettings(direction=gpiod.line.Direction.OUTPUT, output_value=gpiod.line.Value.ACTIVE)}
            comm_pin = chip.request_lines(consumer="remotepi", config=comm_config_out)            
            time.sleep(0.125)
            # change the output to low level for 200ms
            comm_pin.set_value(COMM_PIN, gpiod.line.Value.INACTIVE)
            time.sleep(0.2)
            # change the output to high level for 400ms
            comm_pin.set_value(COMM_PIN, gpiod.line.Value.ACTIVE)
            time.sleep(0.4)
            # change the output to low level
            comm_pin.set_value(COMM_PIN, gpiod.line.Value.INACTIVE)
            # set GPIO 14 high to feedback shutdown to RemotePi Board
            # because the irswitch.sh has already been terminated
            shutdown_config_out = {SHUTDOWN_PIN: gpiod.LineSettings(direction=gpiod.line.Direction.OUTPUT, output_value=gpiod.line.Value.ACTIVE)}
            shutdown_pin = chip.request_lines(consumer="remotepi", config=shutdown_config_out)
            time.sleep(4.0)
        finally:
            comm_pin.release()
            shutdown_pin.release()


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


if gpiod_spec is not None:
    initiate_hw_shutdown_gpiod()
elif rpigpio_spec is not None:
    initiate_hw_shutdown()
else:
    initiate_hw_shutdown_gpiozero()
