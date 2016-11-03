import time
import datetime
import threading

class mt(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self, name="mt")
        self.event_stop = threading.Event()


    def stop(self):
        self.event_stop.set()


    def run(self):
        while not self.event_stop.isSet():
            print("run")
            time.sleep(2)

if __name__ == "__main__":
    t = mt()
    t.start()
    time.sleep(5)
    print(t.isAlive())
    time.sleep(5)
    print(t.isAlive())
    time.sleep(5)
    print(t.isAlive())
    time.sleep(5)
    print(t.isAlive())
    t.stop()
    print(t.isAlive())
    t.join()
    print(t.isAlive())
