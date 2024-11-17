# Batocera RemotePi support

 Because after some Linux kernel changes the integrated support for the RemotePi hardware is currently not working properly, I was asked by RobertMV if I can help to make the already working scripts for LibreELEC work with Batocera as well. The following scripts are the result and tested on real RemotePi hardware with RPi4 and Batocera v40/v41. Many thanks to Robert for testing on real hardware during different troubleshooting sessions. Since I don't own a RemotePi myself, my troubleshooting options are very limited without the help of an owner of this type of hardware. I also assume that the integrated support for the MSL Digital Solutions RemotePi will be corrected in one of the next versions of Batocera.

* /userdata/system/remotepi/irswitch.py
* /userdata/system/remotepi/shutdown.py
* /userdata/system/custom.sh

## Precaution

The integrated support for MSL Digital Solutions RemotePi: "Any remote control as pswitch v2013" or "Any remote control as pswitch v2015" must not be enabled to not conflict with this solution.

## Installation

Connect via SSH/PuTTY to Batocera. You are already in the correct path ***/userdata/system***.

* Download the tar archive directly from the releases at GitHub.

    ```bash
    wget https://github.com/HungerHa/batocera_remotepi/releases/latest/download/remotepi.tgz
    ```

    or copy the ***remotepi.tgz*** via SCP (WinSCP, FileZilla ...) to ***/userdata/system*** if you want.

* Unarchive the scripts. This ensures that the required directories are created and the file permissions are set correctly.

    **ATTENTION**: If a ***custom.sh*** already exists with other customizations, you should first create a backup of this file and adjust the changes again after the installation. The ***custom.sh*** will be replaced by the following process !

    ```bash
    tar -xvzf remotepi.tgz && rm remotepi.tgz
    ```

    Optional: Wget automatically creates a hidden HSTS file (HTTP Strict Transport Security) as a Known Hosts database during the download process. If someone does not like this or is bothered by it, the file can also be removed.

    ```bash
    rm .wget-hsts
    ```

* Activate the background service to observe power button events. Alternatively you can do a **reboot**.

    ```bash
    bash /userdata/system/custom.sh start
    ```

## Uninstallation

Connect via SSH/PuTTY to Batocera. Then stop the running process and delete the scripts including the directory that contains them.

```bash
bash /userdata/system/custom.sh stop
rm -rf /userdata/system/remotepi
```

**ATTENTION**: As mentioned during the installation, the ***custom.sh*** can be a shared file. If you have made additional changes, you may want to make a backup or keep the file. In all other cases, delete this file as well.

```bash
rm custom.sh
```

## Known issues

The content of **custom.sh** was originally intended to work as a Batocera service, as **custom.sh** is deprecated. But during final testing on real hardware, we found that the **remotepi** service was unexpectedly killed during shutdown before it could complete the required communication with the RemotePi hardware. As a workaround, the service was moved back to **custom.sh** to make it reliable.

## Usage as a service

If you are brave and want to ignore the part with the known problems, you can convert the **custom.sh** into **remotepi** service:

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
