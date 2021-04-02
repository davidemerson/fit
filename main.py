""" fit: a productivity logger """
import time
import sys
import os
import uhashlib
import machine
import framebuf
from ssd1306 import SSD1306_I2C

def final_print(sec,final_hash,final_survey):
    """ leaves the summary on the screen before shutting down """
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    short_sec = int(sec)
    duration = (str(hours) + "/" + str(mins) + "/" + str(short_sec))
    oled_show("> fit the"+str(final_hash),str(final_survey),"//"+str(duration))
    time.sleep(30)
    oled_blank()

def timer_down(f_seconds,timer_focus):
    """ counts down for defined period """
    now = time.time()
    end = now + f_seconds
    while now < end:
        now = time.time()
        fit_progress(now,end,timer_focus,f_seconds)
        time.sleep(0.01)
#        if button1.value() == 0:
#             oled_show("","Ended Manually!","")
#             time.sleep(2)
#             break

def timer_up(timer_focus):
    """ counts up for indefinite period """
    now = time.time()
    while True:
        minutes = int((time.time() - now) / 60)
        oled_show(str(timer_focus)," for ",str(minutes))
        time.sleep(0.01)
#         if button1.value() == 0:
#             oled_show("","Ended Manually!","")
#             time.sleep(2)
#             break

def fit_progress(now,end,timer_focus,f_seconds):
    """ tracks progress of a count-down fit and prints to screen """
    remain = end - now
    f_minutes = int((remain)/60)
    j = 1 - (remain / f_seconds)
    pct = int(100*j)
    oled_show(str(timer_focus),str(f_minutes)+" min",str(pct)+"%")

def debounce(btn):
    """ some debounce control """
    count = 2
    while count > 0:
        if btn.value():
            count = 2
        else:
            count -= 1
        time.sleep(.01)

def multi_choice(options):
    """ provides multi-choice menus for two-button navigation """
    for i in options:
        print("below for")
        print("button 1 below for",button1.value())
        print("button 2 below for",button2.value())
        oled_show("      fit",i,"1:sel    2:next")
        while 1:
            print("below while")
            print("button 1 below while",button1.value())
            print("button 2 below while",button2.value())
            b1pressed = button1.value()
            b2pressed = button2.value()
            if b1pressed or b2pressed:
                print("below first if")
                print("button 1 first if",button1.value())
                print("button 2 first if",button2.value())
                break
        if b1pressed:
            print("below second if")
            print("button 1 second if",button1.value())
            print("button 2 second if",button2.value())
            debounce(button1)
            return i
        debounce(button2)

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

def splash_screen():
    oled_show("","      fit","")
    while 1:
        b1pressed = button1.value()
        b2pressed = button2.value()
        if not b1pressed or not b2pressed:
            break

sda = machine.Pin(4)
scl = machine.Pin(5)
i2c = machine.I2C(0,sda=sda, scl=scl, freq=400000)
oled = SSD1306_I2C(128, 32, i2c)

button1 = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
button2 = machine.Pin(27, machine.Pin.IN, machine.Pin.PULL_UP)
#button1 = machine.Pin(2, machine.Pin.IN)
#button2 = machine.Pin(3, machine.Pin.IN)

splash_screen()

print("before f_type")
print("button 1 before f_type",button1.value())
print("button 2 before f_type",button2.value())
F_TYPE = multi_choice(['30 minutes','60 minutes','indefinite'])

print("before f_focus")
print("button 1 before f_focus",button1.value())
print("button 2 before f_focus",button2.value())
F_FOCUS = multi_choice(['personal','work','learning','administration'])

fStart = time.time()

if F_TYPE == "30 minutes":
    timer_down(1800,F_FOCUS)
elif F_TYPE == "60 minutes":
    timer_down(3600,F_FOCUS)
elif F_TYPE == "indefinite":
    timer_up(F_FOCUS)
else:
    sys.exit()

fEnd = time.time()

F_SURVEY = multi_choice(['went well','went ok','went poorly'])

fDuration = fEnd - fStart

F_HASH = uhashlib.sha256(str(fEnd).encode('utf-8')).digest()
F_HASH_SHORT = F_HASH[0:3]

fitdb = open("data.csv","a")
fitdb.write(str(F_HASH)+","+str(F_TYPE)+","+str(F_FOCUS)+","+str(F_SURVEY)+","+str(fStart)+","+str(fEnd)+","+str(fDuration)+"\n")
fitdb.close()

final_print(fDuration,F_HASH_SHORT,F_SURVEY)
