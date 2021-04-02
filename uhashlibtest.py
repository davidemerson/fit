import sys
import os
import hashlib
import time

time_now = "blergh"
hash_test = hashlib.sha256(time_now).hexdigest()

print(time_now)
print(hash_test)