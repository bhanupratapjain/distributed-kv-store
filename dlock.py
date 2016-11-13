import json
import os
import socket
import threading
import time


# The Server that handles locks
# Creates a file with the name of the key
# If the file exists the lock is acquired otherwise not
# Uses a queue to linerize the acquire and release requests
# So basically FCFS
class DlockServer:
    def __init__(self, addr):
        self.dir = os.path.curdir + "/locks"
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(addr)
        self.queue = []
        self.cv = threading.Condition()

    def start(self):
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

        t = threading.Thread(target=self.__process)
        t.start()
        t = threading.Thread(target=self.__listen)
        t.start()

    def __listen(self):
        while True:
            msg, addr = self.socket.recvfrom(1000)
            d = json.loads(msg)
            d['addr'] = addr
            self.cv.acquire()
            self.queue.append(d)
            self.cv.notify()
            self.cv.release()

    def __process(self):
        while True:
            self.cv.acquire()
            if len(self.queue) == 0:
                self.cv.wait()
            msg = self.queue.pop()
            if msg['op'] == 'acquire':
                self.__acquire(msg['key'], msg['addr'])
            else:
                self.__release(msg['key'], msg['addr'])

    def __acquire(self, key, addr):
        if os.path.exists(self.dir + "/" + key):
            self.socket.sendto("Reject", addr)
        else:
            open(self.dir + "/" + key, 'a').close()
            self.socket.sendto("Ok", addr)

    def __release(self, key, addr):
        os.remove(self.dir + "/" + key)
        self.socket.sendto("Ok", addr)


# Wrapper for the requests that will be made to server
class Dlock:
    def __init__(self, server_addr):
        self.addr = server_addr
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def acquire(self, key):
        d = {'op': 'acquire', 'key': key}
        js = json.dumps(d)
        while True:
            self.socket.sendto(js, self.addr)
            res = self.socket.recv(1000)
            print res
            if res == "Ok":
                break
            time.sleep(1)

    def release(self, key):
        d = {"op": 'release', 'key': key}
        js = json.dumps(d)
        self.socket.sendto(js, self.addr)
        res = self.socket.recvfrom(1000)
        if res == "Ok":
            return


if __name__ == "__main__":
    server = DlockServer(('127.0.0.1', 5000))
    server.start()
    time.sleep(1)
    lock = Dlock(('127.0.0.1', 5000))
    lock.acquire('test')
    lock.acquire('bye')
    lock.release('bye')
    lock.acquire('bye')
    lock.release('test')
    lock.acquire('nbjrkenbe')
    lock.release('bye')
