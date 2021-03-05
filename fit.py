import time
import hashlib

def time_convert(sec):
  mins = sec // 60
  sec = sec % 60
  hours = mins // 60
  mins = mins % 60
  print("Duration // {0}.{1}.{2}".format(int(hours),int(mins),int(sec)))

def timerDown(fSeconds):
	elapsed = 0
	while elapsed < fSeconds:
		now = time.time()
		elapsed = now - start_time
		print("{0} since start.".format(elapsed))

def timerUp():
	n = None
	while n != "1":
		n = raw_input("Press 1 to stop >> ")

fType = raw_input("ft30, ft60, or ftcu? >> ")

fStart = time.time()

if fType == "ft30":
	timerDown(2)
elif fType == "ft60":
	timerDown(10)
elif fType == "ftcu":
	timerUp()
else:
	print("Sorry, that's not an option yet.")

fEnd = time.time()

time_elapsed = fEnd - fStart
fHash = hashlib.md5(b'time_elapsed')

time_convert(time_elapsed)
print("This concludes fit the {0}".format(fHash))