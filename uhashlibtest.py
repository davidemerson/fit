import sys
import os
import uhashlib
import time

time_now = "blergh"
hash_test = uhashlib.sha256(time_now).digest()

print(time_now)
print(hash_test)