import threading
import time
from random import randint


class TestLog:
    def __init__(self, server):
        self.server = server
        self.loop_count = 100
        self.max_key = 4

    def start(self):
        t_set1 = threading.Thread(target=self.set_values)
        t_set2 = threading.Thread(target=self.set_values)
        t_set3 = threading.Thread(target=self.set_values)
        t_set1.start()
        t_set2.start()
        t_set3.start()
        t_set1.join()
        t_set2.join()
        t_set3.join()

    def set_values(self):
        index = 0
        while index < self.loop_count:
            self.server.append(str(randint(0, self.max_key)), str(randint(0, self.max_key)))
            self.server.increase_commit_index()
            index += 1
            time.sleep(0.01)
        print "set over\n"
