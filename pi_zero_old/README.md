# fit

fit is a time logger for personal productivity

https://nnix.com/fit/index.gmi

## Configure a pi zero w for this

- Get Rasbian Lite from here https://www.raspberrypi.org/software/operating-systems/
- Flash it onto an SD card.
- Mount the flashed SD card.
- Create the SSH file to enable SSH

```
touch /ssh
```
- Create the wifi configuration
```
touch /wpa_supplicant.conf
```
- Insert the following into wpa_supplicant:
```
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="NETWORK-NAME"
    psk="NETWORK-PASSWORD"
}
```
- Boot the pi, figure out what IP it took on your local network.
- ssh pi@[ip it took]
- Default password is "raspberry" but that's some crap so...
- Change default password on pi user:
```
passwd
```
- then update the distro
```
sudo apt update && sudo apt upgrade -y
```
- replace /boot/config.txt with the config.txt in the repo here
- then configure the thing
```
sudo raspi-config
```
- set your hostname to something sane
- also expand the filesystem to make sure you're using the SD card.
- finally, update the firmware on your device in raspi-config.
- reboot
```
sudo reboot
```
- usermod stuff for spi
```
sudo usermod -a -G i2c,spi,gpio pi
```
- get some python and stuff up in this thing
```
sudo apt install -y python3-dev python-smbus i2c-tools python3-pil python3-pip python3-setuptools python3-rpi.gpio git python3-pip libfreetype6-dev libjpeg-dev libsdl-dev libportmidi-dev libsdl-ttf2.0-dev libsdl-mixer1.2-dev libsdl-image1.2-dev libatlas-base-dev screen
```
- get the waveshare eink repo
```
git clone https://github.com/waveshare/e-Paper.git
```
- get some python packages
```
sudo pip3 install spidev numpy
```
- run the waveshare example from the repo
```
sudo python3 epd_2in13_V2_test.py
```