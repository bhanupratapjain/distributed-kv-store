import socket
import threading

import time

from request_parser import ProtoParser
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
            #parts = request_parser.ProtoParser.parse(msg)
            #t = threading.Thread(target=self.__process,
            #                     args=(clientsocket, parts))
            while(not msg.endswith("\r\n")):
                msg = msg + clientsocket.recv(constants.BUFFER_SIZE)
            t = threading.Thread(target=self.__process_block,
                                 args=(clientsocket,msg))
            t.start()

    def __process_block(self, clientsocket, msg):
        t = ProtoParser.parse_first_line(msg)
        operation = t.iterkeys().next()
        if operation == "set":
            bytes = t[operation][1]
            key = t[operation][0]
            print "bytes", bytes
            val = clientsocket.recv(bytes)
            self.set(key,val)
            clientsocket.send("STORED\r\n")
        elif operation == "get":
            res = ""
            for parts in t[operation]:
                value = str(self.get(parts[0]))
                res = res+"VALUE "+parts[0]+" 0 "+len(value)+"\r\n"+value+"\r\n"
            clientsocket.send(res)
            print res

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
