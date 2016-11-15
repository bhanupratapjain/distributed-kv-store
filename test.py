import threading
import time
from random import randint


class Test:
    def __init__(self, server):
        self.server = server

    def start(self):
        t_set1 = threading.Thread(target=self.set_values)
        t_get1 = threading.Thread(target=self.get_values)
        t_set2 = threading.Thread(target=self.set_values)
        t_get2 = threading.Thread(target=self.get_values)
        t_set3 = threading.Thread(target=self.set_values)
        t_get3 = threading.Thread(target=self.get_values)
        t_set1.join()
        t_get1.join()
        t_set2.join()
        t_get2.join()
        t_set3.join()
        t_get3.join()

    def set_values(self):
        index = 0
        while index < 10000:
            self.server.set(str(randint(0, 5000)), str(randint(0, 5000)))
            index += 1
            time.sleep(0.05)

    def get_values(self):
        index = 0
        while index < 10000:
            self.server.get(str(randint(0, 5000)), str(randint(0, 5000)))
            index += 1
            time.sleep(0.05)
