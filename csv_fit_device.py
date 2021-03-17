import time
import sys
import os
import hashlib
import csv
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'eink')
if os.path.exists(libdir):
    sys.path.append(libdir)
from eink import epd2in13_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

def final_print(sec,fHash_short,fSurvey):
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
	time_draw.text((0, 0), "> fit the "+str(fHash_short), font = font36, fill = 0)
	time_draw.text((20, 50), "> went "+str(fSurvey), font = font18, fill = 0)
	time_draw.text((20, 70), "> lasted //"+str(duration), font = font18, fill = 0)
	epd.displayPartial(epd.getbuffer(time_image))

def timerDown(fSeconds,fFocus):
	now = time.time()
	end = now + fSeconds
	while now < end:
		try:
			now = time.time()
			fitProgress(now,end,fFocus,fSeconds)
			time.sleep(2)
		except KeyboardInterrupt:
			print("\n\nEnded.")
			break

def timerUp(fFocus):
	now = time.time()
	while True:
		try:
			minutes = int((time.time() - now) / 60)
			epd = epd2in13_V2.EPD()
			font42 = ImageFont.truetype("futura_pt_heavy.ttf", 42)
			font18 = ImageFont.truetype("futura_pt_heavy.ttf", 18)
			time_image = Image.new('1', (epd.height, epd.width), 255)
			time_draw = ImageDraw.Draw(time_image)
			epd.init(epd.PART_UPDATE)
			time_draw.rectangle((0, 0, 220, 105), fill = 255)
			time_draw.text((0, 0), "> fit", font = font36, fill = 0)
			time_draw.text((20, 50), "> "+str(fFocus), font = font18, fill = 0)
			time_draw.text((20, 70), "> indefinite", font = font18, fill = 0)
			time_draw.text((170, 30), ":"+str(minutes), font = font42, fill = 0)
			epd.displayPartial(epd.getbuffer(time_image))
			time.sleep(2)
		except KeyboardInterrupt:
			print("\n\nEnded.")
			break

def fitProgress(now,end,fFocus,fSeconds):
	remain = end - now
	fMinutes = int((remain)/60)
	j = 1 - (remain / fSeconds)
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
	time_draw.text((20, 50), "> "+str(fFocus), font = font18, fill = 0)
	time_draw.text((20, 70), "> :"+str(fMinutes)+" remain", font = font18, fill = 0)
	time_draw.text((140, 30), str(pct)+"%", font = font42, fill = 0)
	epd.displayPartial(epd.getbuffer(time_image))

def ink_print(string):
	epd = epd2in13_V2.EPD()
	font18 = ImageFont.truetype("futura_pt_heavy.ttf", 18)
	time_image = Image.new('1', (epd.height, epd.width), 255)
	time_draw = ImageDraw.Draw(time_image)
	epd.init(epd.PART_UPDATE)
	time_draw.rectangle((0, 0, 220, 105), fill = 255)
	time_draw.text((0, 0), str(string), font = font18, fill = 0)
	epd.displayPartial(epd.getbuffer(time_image))

def ink_clear():
	epd = epd2in13_V2.EPD()
	epd.init(epd.FULL_UPDATE)
	epd.Clear(0xFF)

while True:
	try:
		fType = int(input("\n1. 30-minute fit \n2. 60-minute fit \n3. count-up fit \n\n >> "))
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
		fFocus = int(input("\n1. personal fit \n2. work fit \n3. learn fit \n4. admin fit \n\n >> "))
	except ValueError:
		ink_clear()
		ink_print("Sorry, that's not an option.")
		continue
	if fFocus not in [1,2,3,4]:
		ink_clear()
		ink_print("Please select 1, 2, 3 or 4.")
	else:
		break

if fFocus == 1:
	fFocus = "personal"
elif fFocus == 2:
	fFocus = "work"
elif fFocus == 3:
	fFocus = "learn"
elif fFocus == 4:
	fFocus = "admin"
else:
	fFocus = "other"

fStart = time.time()

if fType == 1:
	ink_clear()
	timerDown(1800,fFocus)
elif fType == 2:
	ink_clear()
	timerDown(3600,fFocus)
elif fType == 3:
	ink_clear()
	timerUp(fFocus)
else:
	exit()

fEnd = time.time()

while True:
	try:
		fSurvey = str(input("\nsuccess? (+ / = / -) \n\n>> "))
	except ValueError:
		ink_clear()
		ink_print("Sorry, that's not an option.")
		continue
	if fSurvey not in ["+","=","-"]:
		ink_clear()
		ink_print("Please answer '+', '=', or '-'")
	else:
		break

fDuration = fEnd - fStart

fHash = hashlib.md5(str(fEnd).encode('utf-8')).hexdigest()
fHash_short = fHash[0:5]

#fields = ['fHash','fHash_short','fType','fFocus','fSurvey','fStart','fEnd','fDuration']

fields=[fHash,fHash_short,fType,fFocus,fSurvey,fStart,fEnd,fDuration]
with open(r'fDB.csv', 'a') as f:
    writer = csv.writer(f)
    writer.writerow(fields)

final_print(fDuration,fHash_short,fSurvey)