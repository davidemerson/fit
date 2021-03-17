""" fit: a productivity logger """
import time
import sys
import os
import hashlib
import csv
from PIL import Image,ImageDraw,ImageFont
from eink import epd2in13_V2
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'eink')
if os.path.exists(libdir):
    sys.path.append(libdir)

def final_print(sec,final_hash,final_survey):
    """ leaves the summary on the screen before shutting down """
    epd = epd2in13_V2.EPD()
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    short_sec = int(sec)
    duration = (str(hours) + "/" + str(mins) + "/" + str(short_sec))
    font36 = ImageFont.truetype("futura_pt_heavy.ttf", 36)
    font18 = ImageFont.truetype("futura_pt_heavy.ttf", 18)
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)
    epd.init(epd.PART_UPDATE)
    time_draw.rectangle((0, 0, 220, 105), fill = 255)
    time_draw.text((0, 0), "> fit the "+str(final_hash), font = font36, fill = 0)
    time_draw.text((20, 50), "> went "+str(final_survey), font = font18, fill = 0)
    time_draw.text((20, 70), "> lasted //"+str(duration), font = font18, fill = 0)
    epd.displayPartial(epd.getbuffer(time_image))

def timer_down(f_seconds,timer_focus):
    """ counts down for defined period """
    now = time.time()
    end = now + f_seconds
    while now < end:
        try:
            now = time.time()
            fit_progress(now,end,timer_focus,f_seconds)
            time.sleep(2)
        except KeyboardInterrupt:
            print("\n\nEnded.")
            break

def timer_up(timer_focus):
    """ counts up for indefinite period """
    now = time.time()
    while True:
        try:
            minutes = int((time.time() - now) / 60)
            epd = epd2in13_V2.EPD()
            font42 = ImageFont.truetype("futura_pt_heavy.ttf", 42)
            font36 = ImageFont.truetype("futura_pt_heavy.ttf", 36)
            font18 = ImageFont.truetype("futura_pt_heavy.ttf", 18)
            time_image = Image.new('1', (epd.height, epd.width), 255)
            time_draw = ImageDraw.Draw(time_image)
            epd.init(epd.PART_UPDATE)
            time_draw.rectangle((0, 0, 220, 105), fill = 255)
            time_draw.text((0, 0), "> fit", font = font36, fill = 0)
            time_draw.text((20, 50), "> "+str(timer_focus), font = font18, fill = 0)
            time_draw.text((20, 70), "> indefinite", font = font18, fill = 0)
            time_draw.text((170, 30), ":"+str(minutes), font = font42, fill = 0)
            epd.displayPartial(epd.getbuffer(time_image))
            time.sleep(2)
        except KeyboardInterrupt:
            print("\n\nEnded.")
            break

def fit_progress(now,end,timer_focus,f_seconds):
    """ tracks progress of a count-down fit and prints to screen """
    remain = end - now
    f_minutes = int((remain)/60)
    j = 1 - (remain / f_seconds)
    pct = int(100*j)
    epd = epd2in13_V2.EPD()
    font42 = ImageFont.truetype("futura_pt_heavy.ttf", 42)
    font36 = ImageFont.truetype("futura_pt_heavy.ttf", 36)
    font18 = ImageFont.truetype("futura_pt_heavy.ttf", 18)
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)
    epd.init(epd.PART_UPDATE)
    time_draw.rectangle((0, 0, 220, 105), fill = 255)
    time_draw.text((0, 0), "> fit", font = font36, fill = 0)
    time_draw.text((20, 50), "> "+str(timer_focus), font = font18, fill = 0)
    time_draw.text((20, 70), "> :"+str(f_minutes)+" remain", font = font18, fill = 0)
    time_draw.text((140, 30), str(pct)+"%", font = font42, fill = 0)
    epd.displayPartial(epd.getbuffer(time_image))

def ink_print(string):
    """ displays a string on the eink display """
    epd = epd2in13_V2.EPD()
    font18 = ImageFont.truetype("futura_pt_heavy.ttf", 18)
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)
    epd.init(epd.PART_UPDATE)
    time_draw.rectangle((0, 0, 220, 105), fill = 255)
    time_draw.text((0, 0), str(string), font = font18, fill = 0)
    epd.displayPartial(epd.getbuffer(time_image))

def ink_clear():
    """ clears the eink display """
    epd = epd2in13_V2.EPD()
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)

while True:
    try:
        fType = int(input("\n1. 30-minute fit \n2. 60-minute fit \n3. \
            count-up fit \n\n >> "))
    except ValueError:
        ink_clear()
        ink_print("Sorry, that's not an option.")
        continue
    if fType not in [1,2,3]:
        ink_clear()
        ink_print("Please select 1, 2, 3 or 4.")
    else:
        break

while True:
    try:
        F_FOCUS = int(input("\n1. personal fit \n2. work fit \n3. learn fit \
            \n4. admin fit \n\n >> "))
    except ValueError:
        ink_clear()
        ink_print("Sorry, that's not an option.")
        continue
    if F_FOCUS not in [1,2,3,4]:
        ink_clear()
        ink_print("Please select 1, 2, 3 or 4.")
    else:
        break

if F_FOCUS == 1:
    F_FOCUS = "personal"
elif F_FOCUS == 2:
    F_FOCUS = "work"
elif F_FOCUS == 3:
    F_FOCUS = "learn"
elif F_FOCUS == 4:
    F_FOCUS = "admin"
else:
    F_FOCUS = "other"

fStart = time.time()

if fType == 1:
    ink_clear()
    timer_down(1800,F_FOCUS)
elif fType == 2:
    ink_clear()
    timer_down(3600,F_FOCUS)
elif fType == 3:
    ink_clear()
    timer_up(F_FOCUS)
else:
    sys.exit()

fEnd = time.time()

while True:
    try:
        F_SURVEY = str(input("\nsuccess? (+ / = / -) \n\n>> "))
    except ValueError:
        ink_clear()
        ink_print("Sorry, that's not an option.")
        continue
    if F_SURVEY not in ["+","=","-"]:
        ink_clear()
        ink_print("Please answer '+', '=', or '-'")
    else:
        break

fDuration = fEnd - fStart

F_HASH = hashlib.md5(str(fEnd).encode('utf-8')).hexdigest()
F_HASH_SHORT = F_HASH[0:5]

fields=[F_HASH,F_HASH_SHORT,fType,F_FOCUS,F_SURVEY,fStart,fEnd,fDuration]
with open(r'fDB.csv', 'a') as f:
    writer = csv.writer(f)
    writer.writerow(fields)

final_print(fDuration,F_HASH_SHORT,F_SURVEY)
