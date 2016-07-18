import os
import sys
import datetime
import time

#value = "18:48:00"
#t1 = time.strptime(value, "%H:%M:%S")
#print(t1)
#t20 = datetime.datetime.strptime(value, "%H:%M:%S")
#print(20)


#t10 = datetime.datetime.now()
#time.sleep(2)
#t11 = datetime.datetime.now()
#time.sleep(2)
#t12 = datetime.datetime.now()

#print(t10)
#print(t11)
#print(t12)

#t = t10 - t11
#print(t, t.seconds)

#t = t12 - t11
#print(t, t.seconds)

#t13 = datetime.datetime.today()
#print(t13.weekday())


#weekDay = "0, 1, 2, 3, 4, 5, 6"

#weekDay = tuple(int(item.strip("([ '])")) for item in weekDay.split(",") if item.strip())

#if len(weekDay) > 7:    raise Exception()
#if not all(day < 7 for day in weekDay): raise Exception()

#day = 5

#if any(day == value for value in weekDay):
#    print ("XXX")


#print (weekDay)

v1 = (128, 0, 0)
v2 = (255, 255, 255)

print (v1)
print (v2)

v3 = v2[0] - v1[0]
print (v3)