import threading
import time
from random import randint


class Test:
    def __init__(self, server):
        self.server = server
        self.loop_count = 1000
        self.max_key = 500

    def start(self):
        t_set1 = threading.Thread(target=self.set_values)
        t_get1 = threading.Thread(target=self.get_values)
        t_set2 = threading.Thread(target=self.set_values)
        t_get2 = threading.Thread(target=self.get_values)
        t_set3 = threading.Thread(target=self.set_values)
        t_get3 = threading.Thread(target=self.get_values)
        t_set1.start()
        t_get1.start()
        t_set2.start()
        t_get2.start()
        t_set3.start()
        t_get3.start()
        t_set1.join()
        t_get1.join()
        t_set2.join()
        t_get2.join()
        t_set3.join()
        t_get3.join()

    def set_values(self):
        index = 0
        while index < self.loop_count:
            self.server.set(str(randint(0, self.max_key)), str(randint(0, self.max_key)))
            index += 1
            time.sleep(0.01)
        print "set over\n"

    def get_values(self):
        index = 0
        while index < self.loop_count:
            self.server.get(str(randint(0, self.max_key)))
            index += 1
            time.sleep(0.01)
        print "get over\n"
