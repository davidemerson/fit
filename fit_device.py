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

def time_convert(sec):
	mins = sec // 60
	sec = sec % 60
	hours = mins // 60
	mins = mins % 60
	print("\nduration //{0}/{1}/{2}".format(int(hours),int(mins),sec))

def timerDown(fSeconds,fFocus):
	for i in range(fSeconds):
		fitProgress(i,fSeconds,fFocus)
		time.sleep(1)

def fitProgress(i,fSeconds,fFocus):
	n_bar = 30
	j = i/fSeconds
	epd = epd2in13_V2.EPD()
	epd.init(epd.FULL_UPDATE)
	epd.Clear(0xFF)
	font36 = ImageFont.truetype("futura_pt_heavy.ttf", 36)
	time_image = Image.new('1', (epd.height, epd.width), 255)
	time_draw = ImageDraw.Draw(time_image)
	epd.init(epd.PART_UPDATE)
	num = 0
	time_draw.rectangle((0, 0, 220, 105), fill = 255)
	time_draw.text((0, 0), "fit "+str(i)+" seconds", font = font36, fill = 0)
	epd.displayPartial(epd.getbuffer(time_image))
	# >{'█' * int(n_bar * j):{n_bar}s}< {int(100 * j)}% {fFocus}

def timerUp():
	n = None
	while n != "1":
		n = input("\nPress 1 to stop >> ")

def ink():
	epd = epd2in13_V2.EPD()
	font15 = ImageFont.truetype("futura_pt_heavy.ttf", 15)
	font36 = ImageFont.truetype("futura_pt_heavy.ttf", 36)
	time_image = Image.new('1', (epd.height, epd.width), 255)
	time_draw = ImageDraw.Draw(time_image)
	epd.init(epd.PART_UPDATE)
	num = 0
	while (True):
		time_draw.rectangle((0, 0, 220, 105), fill = 255)
		time_draw.text((0, 0), time.strftime('%H:%M:%S'), font = font36, fill = 0)
		epd.displayPartial(epd.getbuffer(time_image))
		num = num + 1
		if(num == 5):
			break
	epd.init(epd.FULL_UPDATE)
	epd.Clear(0xFF)
	epd.sleep()
	epd2in13_V2.epdconfig.module_exit()

while True:
	try:
		fType = int(input("\n1. 30-minute fit \n2. 60-minute fit \n3. count-up fit \n\n >> "))
	except ValueError:
		print("\nThat's not an option.\n")
		continue
	if fType not in [1,2,3]:
		print("\nPlease select 1, 2, or 3.")
	else:
		break

while True:
	try:
		fFocus = int(input("\n1. personal fit \n2. work fit \n3. learning fit \n4. administrative fit \n\n >> "))
	except ValueError:
		print("\nThat's not an option.\n")
		continue
	if fFocus not in [1,2,3,4]:
		print("\nPlease select 1, 2, 3 or 4.")
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
	timerDown(1800,fFocus)
elif fType == 2:
	timerDown(3600,fFocus)
elif fType == 3:
	timerUp()
else:
	print("Sorry, that's not an option yet.")

fEnd = time.time()

while True:
	try:
		fSurvey = str(input("\nsuccess? (+ / = / -) \n\n>> "))
	except ValueError:
		print("\nThat's not an option.\n")
		continue
	if fSurvey not in ["+","=","-"]:
		print("\nPlease answer '+', '=', or '-'")
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

time_convert(fDuration)
print("\nend of fit the {0}\n".format(fHash_short))