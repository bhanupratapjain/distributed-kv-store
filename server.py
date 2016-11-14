import socket
import threading
import time
from keystore import KeyStore
from random import randint
from request_parser import ProtoParser

class Server:
    def __init__(self, sip, sport, lbip, lbport):
        # create an INET, STREAMing socket
        self.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.ip = sip
        self.port = sport
        self.lb_ip = lbip
        self.lb_port = lbport
        # self.store = dict()  # KeyStore
        self.store = KeyStore(sport)  # KeyStore

    # def register(self):
        # self.

    def start(self):
        self.socket.bind((self.ip, self.port))
        self.socket.listen(5)
        while 1:
            (clientsocket, address) = self.socket.accept()
            # ct = client_thread(clientsocket)
            # ct.run()
            msg = clientsocket.recv(1000)
            parts = msg.split()
            # ProtoParser.parse()

            if parts[0] == "set":
                self.set(parts[1], parts[2])
                clientsocket.send("Done")
            elif parts[0] == "get":
                value = self.get(parts[1])
                clientsocket.send(value)

    def stop(self):
        pass

    # Calls Keystores API
    def get(self, key):
        return self.store.get(key)

    # Same
    def set(self, key, value):
        self.store.set(key, value)
class Test:
    def __init__(self,server):
        self.server = server

    def start(self):
        t_set1 = threading.Thread(target=set.set_values)
        t_get1 = threading.Thread(target=set.get_values)
        t_set2 = threading.Thread(target=set.set_values)
        t_get2 = threading.Thread(target=set.get_values)
        t_set3 = threading.Thread(target=set.set_values)
        t_get3 = threading.Thread(target=set.get_values)
        t_set1.join()
        t_get1.join()
        t_set2.join()
        t_get2.join()
        t_set3.join()
        t_get3.join()

    def set_values(self):
        index = 0
        while(index < 10000):
            self.server.set(str(randint(0, 5000)), str(randint(0, 5000)))
            index = index + 1
            time.sleep(0.05)


    def get_values(self):
        index = 0
        while (index < 10000):
            self.server.get(str(randint(0, 5000)), str(randint(0, 5000)))
            index = index + 1
            time.sleep(0.05)


if __name__ == "__main__":
    server = Server("127.0.0.1", 5003, "127.0.0.1",6003)
    server.start()
    #t =  Test(server)
    #t.start()
