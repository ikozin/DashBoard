import datetime
import time

value = "18:48:00"

t1 = time.strptime(value, "%H:%M:%S")
print(t1)


t2 = datetime.datetime.now()
print(t2)

t3 = datetime.datetime.today()
print(t3)

t5 = datetime.datetime.strptime(value, "%H:%M:%S")
print(t5)

t6 = t5 - t3
print(t6, t6.seconds)


