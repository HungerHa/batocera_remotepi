# Batocera RemotePi support

 I was asked by RobertMV if I can support to get the already working scripts for LibreELEC to work with Batocera too. The following scripts are the result and tested on real RemotePi hardware with RPi4 and Batocera v40/v41. Many thanks to Robert for testing on real hardware during different troubleshooting sessions. I doesn't own a RemotePi by myself, so my chance to troubleshoot without help of an owner of this kind of hardware is very limited. Also I assume, that in one of the next releases of Batocera the integrated support for MSL Digital Solutions RemotePi will be fixed.

* irswitch.py
* shutdown.py
* custom.sh

## Installation

Connect via SSH/PuTTY to Batocera. You are already in the correct path ***/userdata/system***.

* Download the tar archive directly from the releases at GitHub.

    ```bash
    wget https://github.com/HungerHa/batocera_remotepi/releases/latest/download/remotepi.tgz
    ```

    or copy the ***remotepi.tgz*** via SCP (WinSCP, FileZilla ...) to ***/userdata/system*** if you want.

* Unarchive the scripts. This ensures that the required directories are created and the file permissions are set correctly.

    ```bash
    tar -xvzf remotepi.tgz && rm remotepi.tgz
    ```

* Activate the background service to observe power button events. Alternatively you can do a **reboot**.

    ```bash
    bash /userdata/system/custom.sh start
    ```

## Uninstallation

Connect via SSH/PuTTY to Batocera.

```bash
bash /userdata/system/custom.sh stop
rm -rf /userdata/system/remotepi
rm custom.sh
```

## Known issues

The content of **custom.sh** was originally intended to work as a Batocera service, as **custom.sh** is deprecated. But during final testing on real hardware, we found that the **remotepi** service was unexpectedly killed during shutdown before it could complete the required communication with the RemotePi hardware. As a workaround, the service was moved back to **custom.sh** to make it reliable.

## Usage as a service

If you are brave and wan't to ignore the known issues part, you can convert the **custom.sh** to **remotepi** service:

```bash
bash /userdata/system/custom.sh stop
mkdir /userdata/system/services/
mv custom.sh /userdata/system/services/remotepi
batocera-services enable remotepi
batocera-services start remotepi
```

To check if the service is available and running

```bash
batocera-services list
```

```bash
batocera-services status remotepi
```
