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
apt update && apt upgrade -y
```
- then configure the thing
```
sudo raspi-config
```
- enable the SPI interface (this display uses SPI by default, unless you want to desolder some resistors)
- while you're in there, also reduce the GPU memory to 16MB, since you don't need any for this stuff.
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
sudo apt install -y python3-dev python-smbus i2c-tools python3-pil python3-pip python3-setuptools python3-rpi.gpio git python-pip libfreetype6-dev libjpeg-dev libsdl-dev libportmidi-dev libsdl-ttf2.0-dev libsdl-mixer1.2-dev libsdl-image1.2-dev

- upgrade pip
```
sudo -H pip3 install --upgrade pip
```
- install luma.oled
```
sudo -H pip3 install --upgrade luma.oled
```
- Get the driver info at https://www.waveshare.com/wiki/2.23inch_OLED_HAT
```
wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.60.tar.gz
tar zxvf bcm2835-1.60.tar.gz
cd bcm2835-1.60/
sudo ./configure
sudo make
sudo make check
sudo make install
```
- get luma examples
```
git clone https://github.com/rm-hull/luma.examples.git
cd luma.examples/examples
```
