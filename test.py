import os
import sys
import datetime
import time

#value = "18:48:00"
#t1 = time.strptime(value, "%H:%M:%S")
#print(t1)
#t20 = datetime.datetime.strptime(value, "%H:%M:%S")
#print(20)


t10 = datetime.datetime.now()
time.sleep(2)
t11 = datetime.datetime.now()
time.sleep(2)
t12 = datetime.datetime.now()

print(t10)
print(t11)
print(t12)

t = t10 - t11
print(t, t.seconds)

t = t12 - t11
print(t, t.seconds)
