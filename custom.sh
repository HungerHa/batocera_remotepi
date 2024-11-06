#!/bin/bash
case "$1" in
    start)
        # Code in here will only be executed on boot.
        echo -n "Starting the RemotePi IR/power button observer."
        /userdata/system/irswitch.py &
        ;;
    stop)
        # Code in here will only be executed on shutdown.
        echo -n "Signalling the shutdown to RemotePi."
        ps -ef | grep 'irswitch\.' | grep -v grep | awk '{print $2}' | xargs -r kill -15
        /userdata/system/shutdown.py
        ;;
    restart|reload)
        # Code in here will executed (when?).
        ;;
    *)
        # Code in here will be executed in all other conditions.
        echo "Usage: $0 {start|stop|restart}"
        ;;
esac
 
exit $?
