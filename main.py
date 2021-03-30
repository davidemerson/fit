""" fit: a productivity logger """
import time
import sys
import os
import uhashlib
import machine
from ssd1306 import SSD1306_I2C
import framebuf

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
    count = 2
    while count > 0:
        if btn.value():
            count = 2
        else:
            count -= 1
        time.sleep(0.01)
    
def multi_choice(options):
    for i in options:
        oled_show("> fit",i,"1:yes  2:next")
        # Wait for any button press.
        while 1:
            b1pressed = button1.value()
            b2pressed = button2.value()
            if b1pressed or b2pressed: 
                break
        if b1pressed:
            print( i, "chosen" )
            debounce(button1)
            return i
        # We know B2 was pressed.
        debounce(button2)

def oled_show(message1,message2,message3):
    """ displays a three line message """
    oled.fill(0) # clear the display
    oled.text(message1,5,5)
    oled.text(message2,5,15)
    oled.text(message3,5,25)
    oled.show()

def oled_blank():
    """ blanks the oled display to avoid burn in """
    oled.fill(0)
    oled.show()

""" oled configuration """
sda=machine.Pin(4)
scl=machine.Pin(5)
i2c=machine.I2C(0,sda=sda, scl=scl, freq=400000)
oled = SSD1306_I2C(128, 32, i2c)

oled_show("I","like","chinese")
button1 = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
button2 = machine.Pin(3, machine.Pin.IN, machine.Pin.PULL_UP)

fType = multi_choice(['30-minute fit','60-minute fit','indefinite fit'])

F_FOCUS = multi_choice(['personal fit','work fit','learn fit','admin fit'])

fStart = time.time()

if fType == "30-minute fit":
    timer_down(1800,F_FOCUS)
elif fType == "60-minute fit":
    timer_down(3600,F_FOCUS)
elif fType == "indefinite fit":
    timer_up(F_FOCUS)
else:
    sys.exit()

fEnd = time.time()

F_SURVEY = multi_choice(['went well','went ok','went poorly'])

fDuration = fEnd - fStart

F_HASH = uhashlib.sha256(str(fEnd).encode('utf-8')).digest()
F_HASH_SHORT = F_HASH[0:3]

fitdb = open("data.csv","a")
fitdb.write(str(F_HASH)+","+str(fType)+","+str(F_FOCUS)+","+str(F_SURVEY)+","+str(fStart)+","+str(fEnd)+","+str(fDuration)+"\n")
fitdb.close()

final_print(fDuration,F_HASH_SHORT,F_SURVEY)
