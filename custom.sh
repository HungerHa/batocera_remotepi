#!/bin/bash
#
# Batocera service/custom.sh file for RemotePi power button events
# and graceful shutdown.
#
# Created on: 2024-11-03 16:30
# Changed on: 2024-11-14 18:11
# Author: HarryH
# Version: 1.0.2
#
# Changelog:
# 1.0.2 2024-11-14
# - workaround: renamed back to custom.sh to work reliable on shutdown (not unexpectedly killed)
# - switched to the official method for detecting shutdown in Batocera
# 1.0.1 2024-11-05
# - refactored to work as a batocera-service
# 1.0.0 2024-11-03
# - initial version

case "$1" in
    start)
        echo "Starting the RemotePi IR/power button observer."
        /userdata/system/remotepi/irswitch.py &
        if [ $? -eq 0 ]; then
            logger -t remotepi "IR/power button observer started."
        fi
        ;;
    stop)
        echo "Stopping the RemotePi IR/power button observer."
        ps -ef | grep 'irswitch\.' | grep -v grep | awk '{print $2}' | xargs -r kill -15
        if [ -f "/tmp/shutdown.please" ]; then
            # Code in here will only be executed on shutdown.
            echo "Signalling the shutdown to RemotePi."
            /userdata/system/remotepi/shutdown.py
            logger -t remotepi "Shutdown initiated"
        fi
        logger -t remotepi "IR/power button observer stopped."
        ;;
    status)
        # Code in here will executed on status request.
        irswitch_check=$(ps -ef | grep 'irswitch\.' | grep -v grep)
        if [ $? -eq 0 ]; then
            echo "RemotePi IR/power button observer is running."
        else
            echo "RemotePi IR/power button observer is stopped."
        fi
        ;;
    *)
        # Code in here will be executed in all other conditions.
        echo "Usage: $0 {start|stop|status}"
        ;;
esac
 
exit $?
