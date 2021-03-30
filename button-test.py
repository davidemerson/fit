import machine
import time

button1 = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
button2 = machine.Pin(3, machine.Pin.IN, machine.Pin.PULL_UP)

while True:
    b1pressed = button1.value()
    b2pressed = button2.value()
    time.sleep(0.01)
    b1released = button1.value()
    b2released = button2.value()
    if b1pressed and not b1released:
        print('Button1 pressed!')
    if b2pressed and not b2released:
        print('Button2 pressed!')
    if not b2pressed and b2released:
        print('Button2 released!')
    elif not b1pressed and b1released:
        print('Button1 released!')