import time
import sys
import os
import hashlib
import sqlite3
from sqlite3 import Error

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
	n_bar = 30 #size of progress bar
	j = i/fSeconds
	sys.stdout.write('\r')
	sys.stdout.write(f">{'█' * int(n_bar * j):{n_bar}s}< {int(100 * j)}% {fFocus}")
	sys.stdout.flush()

def timerUp():
	n = None
	while n != "1":
		n = input("\nPress 1 to stop >> ")

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