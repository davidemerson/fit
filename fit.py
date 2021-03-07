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

def create_fit(conn, fit):
    """
    Create a new project into the projects table
    :param conn:
    :param fit:
    :return: fit id
    """
    sql = ''' 
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, fit)
    conn.commit()
    return cur.lastrowid

def time_convert(sec):
  mins = sec // 60
  sec = sec % 60
  hours = mins // 60
  mins = mins % 60
  print("duration //{0}/{1}/{2}".format(int(hours),int(mins),sec))

def timerDown(fSeconds,fFocus):
	elapsed = 0
	while elapsed < fSeconds:
		now = time.time()
		elapsed = now - fStart
		for i in range(fSeconds):
			fitProgress(i,fSeconds,fFocus)
			time.sleep(0.05)  
		#print("{0} since start.".format(elapsed))

def fitProgress(i,max,fFocus):
    n_bar =10 #size of progress bar
    j= i/max
    sys.stdout.write('\r')
    sys.stdout.write(f"[{'=' * int(n_bar * j):{n_bar}s}] {int(100 * j)}%  {fFocus}")
    sys.stdout.flush()

def timerUp():
	n = None
	while n != "1":
		n = input("Press 1 to stop >> ")

fType = input("ft30, ft60, or ftcu? >> ")
fFocus = input("(p)ersonal, (w)ork, (l)earning? >> ")

fStart = time.time()

if fType == "ft30":
	timerDown(1800,fFocus)
elif fType == "ft60":
	timerDown(3600,fFocus)
elif fType == "ftcu":
	timerUp()
else:
	print("Sorry, that's not an option yet.")

fEnd = time.time()

fSurvey = input("success? (+ / = / -) >> ")

fDuration = fEnd - fStart

fHash = hashlib.md5(str(fEnd).encode('utf-8')).hexdigest()
fHash_short = fHash[0:5]

conn = sqlite3.connect("./fDB.db")
c = conn.cursor()
params = (str(fHash),str(fHash_short),str(fType),str(fFocus),str(fSurvey),int(fStart),int(fEnd),fDuration)
conn.execute("INSERT INTO fits (fHash,fHash_short,fType,fFocus,fSurvey,fStart,fEnd,fDuration) VALUES (?,?,?,?,?,?,?)",params)
conn.commit()

time_convert(fDuration)
print("end of fit the {0}".format(fHash_short))