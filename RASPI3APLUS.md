# Setup Raspberry Pi 3 A+
Procedure

1. [Setup](#setup)
    1. [raspi-config](#raspi-config)
    1. [Stops Bluetooth](#stops-bluetooth)
    1. [Allow cgroup V2 CPU & Memory control](#allow-cgroup-v2-cpu--memory-control)
    1. [Extend swap file](#extend-swap-file)
    1. [Fixed IP address](#fixed-ip-address)
1. [Setup I2C](#setup-i2c)
    1. [Check I2C device](#check-i2c-device)
    1. [Allow rootless mode dockers to handle I2C devices](#allow-rootless-mode-dockers-to-handle-i2c-devices)
1. [Install rootless mode docker](#install-rootless-mode-docker)
    1. [Uninstall old versions](#uninstall-old-versions)
    1. [Install using the apt repository](#install-using-the-apt-repository)
    1. [Set the route-less mode](#set-the-route-less-mode)

Raspberry Pi and peripherals

|Items|Value|
|---|---|
|SBC|[Raspberry Pi 3A+](https://www.raspberrypi.com/products/raspberry-pi-3-model-a-plus/)|
|uHAT|[RPZ-IR-Sensor](https://www.indoorcorgielec.com/products/rpz-ir-sensor/)|
|Storage|uSD Card 16GByte|


OS customization - Raspberry Pi OS Lite (64bit) (bookworm)

|Items|propriety|param 1|param 2|param 3|
|---|---|---|---|---|
|Uostname|[X]|amedas|-|-|
|Username|[X]|re|\<PASSWORD\>|-|
|Wi-Fi|[X]|\<SSID\>|\<PASSWORD\>|JP|
|Locale|[X]|Asia/Tokyo|jp|-|
|SSH|[X]|password auth|-|-|

- IP address : 192.168.68.160/24

## Setup

https://www.raspberrypi.com/documentation/computers/configuration.html

### raspi-config
~~~sh
sudo apt update
sudu apt full-upgrade -y
sudo apt autoremove -y

sudo raspi-config nonint do_boot_behaviour B2
sudo raspi-config nonint do_i2c 0
~~~

### Stops Bluetooth

~~~sh
sudo nano /boot/firmware/config.txt
~~~
~~~diff
[all]
+ dtoverlay=disable-bt
~~~

### Allow cgroup V2 CPU & Memory control

~~~sh
stat -fc %T /sys/fs/cgroup/
# > cgroup2fs

sudo nano /boot/firmware/cmdline.txt
~~~
Add to the end of the line without a line break
~~~diff
cgroup_enable=cpuset
cgroup_enable=memory
cgroup_memory=1
swapaccount=1
~~~

### Extend swap file

~~~sh
sudo nano /etc/dphys-swapfile
~~~
~~~diff
- CONF_SWAPSIZE=100
+ CONF_SWAPSIZE=2048
~~~

~~~sh
sudo systemctl restart dphys-swapfile

# check
free -h
~~~

### Fixed IP address

~~~sh
nmcli -t device
# > wlan0:wifi:connected:preconfigured  <= Edit this
# > lo:loopback:connected (externally):lo
# > p2p-dev-wlan0:wifi-p2p:disconnected:

sudo nmcli connection modify preconfigured \
     ifname wlan0 \
     type wifi \
     autoconnect yes \
     ipv4.method manual \
     ipv4.addresses "192.168.68.160/24" \
     ipv4.gateway "192.168.68.1" \
     +ipv4.dns "192.168.68.1"

sudo nmcli connection reload
sudo nmcli connection up preconfigured
~~~

## Setup I2C

### Check I2C device

~~~sh
sudo apt update
sudo apt install i2c-tools -y

# check
i2cdetect -y 1
~~~

### Allow rootless mode dockers to handle I2C devices

~~~sh
sudo nano /etc/udev/rules.d/99-com.rules
~~~
~~~diff
- SUBSYSTEM=="i2c-dev", GROUP="i2c", MODE="0660"
+ SUBSYSTEM=="i2c-dev", GROUP="i2c", MODE="0666"
~~~
~~~sh
sudo udevadm control --reload-rules
~~~

> Add host-side device to container
>> $ docker run --device=/dev/i2c-1:/dev/i2c-1 ...


## Install rootless mode docker

https://docs.docker.com/engine/install/debian/<br>
https://docs.docker.com/engine/security/rootless/

### Uninstall old versions

~~~sh
for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do sudo apt-get remove $pkg; done
~~~

### Install using the apt repository

~~~sh
# Add Docker's official GPG key:
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
~~~

### Set the route-less mode

Installing Related Packages
~~~sh
sudo apt update
sudo apt install -y uidmap
~~~

Install
~~~sh
sudo apt update
sudo apt install -y docker-ce-rootless-extras

dockerd-rootless-setuptool.sh check
dockerd-rootless-setuptool.sh install
~~~

Starting the docker daemon
~~~sh
systemctl --user enable docker
systemctl --user restart docker
~~~
---