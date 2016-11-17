import socket
import threading

import constants
from keystore import KeyStore


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

            # parts = request_parser.ProtoParser.parse(msg)
            # t = threading.Thread(target=self.__process,
            #                     args=(clientsocket, parts))

            t = threading.Thread(target=self.__process_block,
                                 args=(clientsocket,))
            t.start()

    def __process_block(self, clientsocket):
        msg = clientsocket.recv(constants.BUFFER_SIZE)
        print msg
        if msg[:3] == "set":
            while msg.count("\r\n") < 2:
                msg = msg + clientsocket.recv(constants.BUFFER_SIZE)
            parts = msg.split("\r\n")
            key = parts[0].split(" ")[1]
            val = parts[1]
            print msg, key, val
            self.set(key, val)
            clientsocket.send("STORED\r\n")
        elif msg[:3] == "get":
            while (msg.find("\r\n") == -1):
                msg = msg + clientsocket.recv(constants.BUFFER_SIZE)
            res = ""
            parts = msg.strip().split(" ")
            for part in parts[1:]:
                value = self.get(part)
                if value is not None:
                    res = res + "VALUE " + part + " 0 " + str(
                        len(value)) + "\r\n" + str(value) + "\r\n"
            print "get res ", res
            res += "END\r\n"
            clientsocket.send(res)
        clientsocket.close()

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
