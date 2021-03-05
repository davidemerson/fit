import time
import os
import hashlib

def time_convert(sec):
  mins = sec // 60
  sec = sec % 60
  hours = mins // 60
  mins = mins % 60
  print("Duration //{0}/{1}/{2}".format(int(hours),int(mins),sec))

def timerDown(fSeconds):
	elapsed = 0
	while elapsed < fSeconds:
		now = time.time()
		elapsed = now - fStart
		print("{0} since start.".format(elapsed))

def timerUp():
	n = None
	while n != "1":
		n = raw_input("Press 1 to stop >> ")

#need to take input for fFocus

fType = raw_input("ft30, ft60, or ftcu? >> ")

fStart = time.time()

if fType == "ft30":
	timerDown(1800)
elif fType == "ft60":
	timerDown(3600)
elif fType == "ftcu":
	timerUp()
else:
	print("Sorry, that's not an option yet.")

fEnd = time.time()

fDuration = fEnd - fStart

fHash = hashlib.md5(str(fEnd)).hexdigest()
fHash_short = fHash[0:5]

time_convert(fDuration)
print("Concluding fit the {0}".format(fHash_short))