""" fit: a productivity logger """
import time
import sys
import ubinascii
import uhashlib
import machine
from itertools import cycle
from ssd1306 import SSD1306_I2C

def final_print(sec,final_hash,final_survey):
    """ leaves the summary on the screen before shutting down """
    mins = sec // 60
    sec = sec % 60
    mins = int(mins)
    short_sec = int(sec)
    duration = (str(mins)+"'"+str(short_sec)+'"')
    oled_show(str(final_hash)[0:6],str(final_survey),str(duration))
    time.sleep(15)
    oled_blank()

def timer_down(f_seconds,timer_focus):
    """ counts down for defined period """
    now = time.time()
    end = now + f_seconds
    while now < end:
        now = time.time()
        fit_progress(now,end,timer_focus,f_seconds)
        time.sleep(0.01)
        if not button2.value():
            manual_end()
            break

def timer_up(timer_focus):
    """ counts up for indefinite period """
    now = time.time()
    while True:
        minutes = int((time.time() - now) / 60)
        oled_show(str(timer_focus),"for ",str(minutes))
        time.sleep(0.01)
        if not button2.value():
            manual_end()
            break

def manual_end():
    """ notes that process was manually ended """
    oled_show("","Ended!","")
    time.sleep(2)

def fit_progress(now,end,timer_focus,f_seconds):
    """ tracks progress of a count-down fit and prints to screen """
    remain = end - now
    f_minutes = int((remain)/60)
    j = 1 - (remain / f_seconds)
    pct = int(100*j)
    oled_show(str(timer_focus),str(f_minutes)+" min",str(pct)+"%")

def multi_choice(options):
    """ provides multi-choice menus for two-button navigation """
    for i in cycle(options):
        oled_show("fit",i,"1:y 2:n")
        time.sleep(0.5)
        while 1:
            if not button1.value():
                return i
            if not button2.value():
                break

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
    """ displays a startup splash screen """
    oled_show("","  fit","")
    while 1:
        b1pressed = button1.value()
        b2pressed = button2.value()
        if not b1pressed or not b2pressed:
            break

def f_hash_digest(sha):
    """ returns a readable hash """
    return hex(int(ubinascii.hexlify(sha.digest()).decode(), 16))

sda = machine.Pin(4)
scl = machine.Pin(5)
i2c = machine.I2C(0,sda=sda, scl=scl, freq=400000)
oled = SSD1306_I2C(64, 32, i2c)

button1 = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
button2 = machine.Pin(27, machine.Pin.IN, machine.Pin.PULL_UP)
#button1 = machine.Pin(2, machine.Pin.IN)
#button2 = machine.Pin(3, machine.Pin.IN)

splash_screen()

print("before f_type")
print("button 1 before f_type",button1.value())
print("button 2 before f_type",button2.value())
F_TYPE = multi_choice(['30 min','60 min','indef.'])

print("before f_focus")
print("button 1 before f_focus",button1.value())
print("button 2 before f_focus",button2.value())
F_FOCUS = multi_choice(['fdcp','hobby','work','learn','admin'])

fStart = time.time()

if F_TYPE == "30 min":
    timer_down(1800,F_FOCUS)
elif F_TYPE == "60 min":
    timer_down(3600,F_FOCUS)
elif F_TYPE == "indef.":
    timer_up(F_FOCUS)
else:
    sys.exit()

fEnd = time.time()

F_SURVEY = multi_choice(['went +','went =','went -'])

fDuration = fEnd - fStart

F_HASH = uhashlib.sha256(str(fEnd))

F_HASH_SHORT = f_hash_digest(F_HASH)

fitdb = open("data.csv","a")
fitdb.write(str(F_HASH_SHORT)+","+str(F_TYPE)+","+str(F_FOCUS)+","+str(F_SURVEY)+","+str(fStart)+","+str(fEnd)+","+str(fDuration)+"\n")
fitdb.close()

final_print(fDuration,F_HASH_SHORT,F_SURVEY)
