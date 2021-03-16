import time
import sys
import os
import hashlib
import sqlite3
from sqlite3 import Error
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'eink')
if os.path.exists(libdir):
    sys.path.append(libdir)
from eink import epd2in13_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

class DBConnection:

    def __init__(self, dbpath):
        self.connection = sqlite3.connect(dbpath)
        self.cursor = self.connection.cursor()

    def create_table(self, query):
        self.cursor.execute(query)

def main():
    dbpath = f"./fDB.db"
    sql_create_fits_table = """
        CREATE TABLE IF NOT EXISTS fits (
            fHash text PRIMARY KEY,
            fHash_short text NOT NULL,
            fType text NOT NULL,
            fFocus text NOT NULL,
            fSurvey text NOT NULL,
            fStart integer NOT NULL,
            fEnd integer NOT NULL,
            fDuration integer NOT NULL
        ); """
    connection = DBConnection(dbpath)
    connection.create_table(sql_create_fits_table)

if __name__ == '__main__':
    main()

def final_print(sec,fHash_short):
	epd = epd2in13_V2.EPD()
	epd.init(epd.FULL_UPDATE)
	epd.Clear(0xFF)
	mins = sec // 60
	sec = sec % 60
	hours = mins // 60
	mins = mins % 60
	str(duration) = (str(hours) + "/" + str(mins) + "/" + str(sec))
	font42 = ImageFont.truetype("futura_pt_heavy.ttf", 42)
	font36 = ImageFont.truetype("futura_pt_heavy.ttf", 36)
	font18 = ImageFont.truetype("futura_pt_heavy.ttf", 18)
	time_image = Image.new('1', (epd.height, epd.width), 255)
	time_draw = ImageDraw.Draw(time_image)
	epd.init(epd.PART_UPDATE)
	time_draw.rectangle((0, 0, 220, 105), fill = 255)
	time_draw.text((0, 0), "> fit", font = font36, fill = 0)
	time_draw.text((20, 50), "> end of "+str(fHash_short)+"", font = font18, fill = 0)
	time_draw.text((20, 70), "> lasted //"+str(duration)+" ", font = font18, fill = 0)
	time_draw.text((140, 30), ""+str(fHash_short)+"", font = font42, fill = 0)
	epd.displayPartial(epd.getbuffer(time_image))

def timerDown(fSeconds,fFocus):
	now = time.time()
	end = now + fSeconds
	while now < end:
		now = time.time()
		print(now,"now")
		print(end,"end")
		print(fSeconds,"fSeconds")
		fitProgress(now,end,fFocus)
		time.sleep(1)

def fitProgress(now,end,fFocus):
	remain = end - now
	fMinutes = int((remain)/60)
	j = now / end
	print(j, "J")
	print(fMinutes, "fMinutes")
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
	time_draw.text((20, 50), "> "+str(fFocus)+"", font = font18, fill = 0)
	time_draw.text((20, 70), "> :"+str(fMinutes)+" remain", font = font18, fill = 0)
	time_draw.text((140, 30), ""+str(pct)+"%", font = font42, fill = 0)
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

def timerUp():
	n = None
	while n != "1":
		n = input("\nPress 1 to stop >> ")

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
		fFocus = int(input("\n1. personal fit \n2. work fit \n3. learning fit \n4. administrative fit \n\n >> "))
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
	fFocus = "learning"
elif fFocus == 4:
	fFocus = "administrative"
else:
	fFocus = "other"

fStart = time.time()

if fType == 1:
	ink_clear()
	timerDown(15,fFocus)
elif fType == 2:
	ink_clear()
	timerDown(30,fFocus)
elif fType == 3:
	timerUp()
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

conn = sqlite3.connect("./fDB.db")
c = conn.cursor()
params = (str(fHash),str(fHash_short),str(fType),str(fFocus),str(fSurvey),int(fStart),int(fEnd),fDuration)
conn.execute("INSERT INTO fits (fHash,fHash_short,fType,fFocus,fSurvey,fStart,fEnd,fDuration) VALUES (?,?,?,?,?,?,?,?)",params)
conn.commit()

final_print(fDuration,fHash_short)