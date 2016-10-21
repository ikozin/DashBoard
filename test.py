import time
import datetime


if __name__ == "__main__":

    currentTime = datetime.datetime.now()

    text = "Московское время {:%H:%M}".format(currentTime)
    print(text)

    #startTime = datetime.datetime.strptime("9:00:00", "%H:%M:%S")
    #stopTime = datetime.datetime.strptime("20:00:00", "%H:%M:%S")

    #t1 = currentTime - startTime
    #t2 = currentTime - stopTime
    #print(t1.seconds)
    #print(t2.seconds)

    #dtime = datetime.datetime.now()
    #ans_time = time.mktime(dtime.timetuple())
    #print(ans_time)

    #print()
    #print(24*60*60)
    #print()

    #startTime = datetime.datetime.strptime("14:59:00", "%H:%M:%S")
    #print((currentTime.time() > startTime.time()))
    #startTime = datetime.datetime.strptime("15:00:00", "%H:%M:%S")
    #print((currentTime.time() > startTime.time()))
    #startTime = datetime.datetime.strptime("15:01:00", "%H:%M:%S")
    #print((currentTime.time() > startTime.time()))
    #startTime = datetime.datetime.strptime("15:02:00", "%H:%M:%S")
    #print((currentTime.time() > startTime.time()))
    #startTime = datetime.datetime.strptime("15:03:00", "%H:%M:%S")
    #print((currentTime.time() > startTime.time()))
    #startTime = datetime.datetime.strptime("15:04:00", "%H:%M:%S")
    #print((currentTime.time() > startTime.time()))

    #print()
    #print(24*60*60)
    #print()

    #startTime = datetime.datetime.strptime("14:59:00", "%H:%M:%S")
    #print((startTime.time() > currentTime.time()))
    #startTime = datetime.datetime.strptime("15:00:00", "%H:%M:%S")
    #print((startTime.time() > currentTime.time()))
    #startTime = datetime.datetime.strptime("15:01:00", "%H:%M:%S")
    #print((startTime.time() > currentTime.time()))
    #startTime = datetime.datetime.strptime("15:02:00", "%H:%M:%S")
    #print((startTime.time() > currentTime.time()))
    #startTime = datetime.datetime.strptime("15:02:00", "%H:%M:%S")
    #print((startTime.time() > currentTime.time()))
    #startTime = datetime.datetime.strptime("15:04:00", "%H:%M:%S")
    #print((startTime.time() > currentTime.time()))


    #print()
    #print(startTime.time())
    #print()
    #print(currentTime.time())
    #print()

    ##print(ans_time)

    ##print((currentDate - date1).seconds)
    ##print((date1 - currentDate).seconds)
    ##print(3600*24)
    ##print((currentDate - date2).seconds)
    ##print((date2 - currentDate).seconds)
    ##print(3600*24)

    ##list = [ "Main", "Time", "Alarm", "Voice", "YandexNews", "OpenWeatherMap", "WunderGround", "Calendar", "Swap", "Watcher"]
    ##print(list)
    ##item = list.pop(1)
    ##print(item)
    ##print(list)
    ##list.insert(0, item)
    ##print(list)
