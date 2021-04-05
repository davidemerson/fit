import machine
import framebuf
import time
from ssd1306 import SSD1306_I2C

def oled_show(message1,message2,message3):
    """ clears the oled and displays a three line message """
    oled.fill(0)
    oled.text(message1,5,5)
    oled.text(message2,5,15)
    oled.text(message3,5,25)
    oled.show()

def oled_blank():
    """ clears the oled display to avoid burn in """
    oled.fill(0)
    oled.show()

def multi_choice(options):
    """ provides multi-choice menus for two-button navigation """
    for i in options:
        oled_show("      fit",i,"1:sel    2:next")
        time.sleep(0.5)
        while 1:
            if not button1.value():
                return i
            if not button2.value():
                break

sda = machine.Pin(4)
scl = machine.Pin(5)
i2c = machine.I2C(0,sda=sda, scl=scl, freq=400000)
oled = SSD1306_I2C(128, 32, i2c)

button1 = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
button2 = machine.Pin(27, machine.Pin.IN, machine.Pin.PULL_UP)

print("before f_type")
print("button 1 before f_type",button1.value())
print("button 2 before f_type",button2.value())
F_TYPE = multi_choice(['30 minutes','60 minutes','indefinite'])

print(F_TYPE)
#while True:
#    print('Button1 down!') if not button1.value() else print('Button1 up!') 
#    print('Button2 down!') if not button2.value() else print('Button2 up!')
    
