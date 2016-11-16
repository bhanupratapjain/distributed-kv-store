import socket
import threading

import time

import request_parser
from keystore import KeyStore
import constants

class Server:
    def __init__(self, cip, cport, sip, sport, lbip, lbport):
        # create an INET, STREAMing socket
        self.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.sip = sip
        self.sport = sport
        self.cip = cip
        self.cport = cport
        self.lbip = lbip
        self.lbport = lbport
        self.store = KeyStore((self.lbip, self.lbport),
                              (self.cip, self.cport),
                              (self.sip, sport))  # KeyStore

    def start(self):
        threading.Thread(target=self.store.start).start()
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.cip, self.cport))
        self.socket.listen(constants.LEADER_QUEUE_SIZE)
        while 1:
            (clientsocket, address) = self.socket.accept()
            msg = clientsocket.recv(constants.BUFFER_SIZE)
            parts = request_parser.ProtoParser.parse(msg)
            t = threading.Thread(target=self.__process,
                                 args=(clientsocket, parts))
            t.start()

    def __process(self, clientsocket, parts):
        if parts[0] == "set":
            self.set(parts[1], parts[2])
            clientsocket.send("STORED\r\n")
        elif parts[0] == "get":
            value = self.get(parts[1])
            res = "VALUE "+parts[1]+" 0 "+str(value)+"\r\n"
            clientsocket.send(res)

    def stop(self):
        pass

    # Calls Keystores API
    def get(self, key):
        return self.store.get(key)

    # Same
    def set(self, key, value):
        self.store.set(key, value)


if __name__ == "__main__":
    server = Server("127.0.0.1", 5000, "127.0.0.1", 5001, "127.0.0.1", 4501)
    server.start()
    # t =  Test(server)
    # t.start()
