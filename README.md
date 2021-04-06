# fit

fit is a time logger for personal productivity

https://nnix.com/fit/index.gmi

## Configure a microcontroller for this

- Get Raspberry Pi Pico (I used a Tiny2040 from Pimoroni, but there are many which work.)
- Get two momentary normally-open switches, or one double-momentary switch and one SSD1306 OLED (I used 64x32, but you can reformat the graphics if you want to have a larger one).
- Get the MicroPython UF2 from here (https://www.raspberrypi.org/documentation/rp2040/getting-started/#getting-started-with-micropython).
- Flash the UF2 onto the Pi Pico using the instructions which came with it.
- Clone the repo here. In main.py, modify the pins for the buttons to the ones you use on your device. Likewise in main.py, modify the pins for the OLED display to the ones you use on your device.
- In main.py, modify the 
- Copy *.py from this repo onto the Pi Pico (you can use "Thonny" to accomplish this). "main.py" is what will be run when you reboot the Pi.
- Reboot the Pi and check things out.

Note that the program writes a CSV to the flash of the pi, data.csv. You can use Thonny or any other program capable of mounting the Pi Pico flash to read this or download it for analysis.

There are some historical files under "pi_zero_old" folder here. Feel free to use those if you want to use other hardware, such as a Waveshare eink display or a Pi Zero. I originally built this on a Pi Zero, but was frustrated with the overhead of Linux, the display drivers, and the power consumption, so I went way smaller and got a 2040/Pico. I'm much happier with the 2040 as a platform, especially for something this simple.