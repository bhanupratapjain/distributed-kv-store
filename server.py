import socket
import threading

from keystore import KeyStore
import request_parser

class Server:
    def __init__(self, cip, cport, sip, sport, lbip, lbport):
        # create an INET, STREAMing socket
        self.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.sip = sip
        self.sport = sport
        self.cip = cip
        self.cport = cport
        self.lb_ip = lbip
        self.lb_port = lbport
        self.store = KeyStore((self.lb_ip, self.lb_port),
                              (self.cip, self.cport),
                              (self.sip, sport))  # KeyStore

    def start(self):
        self.store.start()
        self.socket.bind((self.sip, self.sport))
        self.socket.listen(5)
        while 1:
            (clientsocket, address) = self.socket.accept()
            msg = clientsocket.recv(1000)
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
            clientsocket.send(value)

    def stop(self):
        pass

    # Calls Keystores API
    def get(self, key):
        return self.store.get(key)

    # Same
    def set(self, key, value):
        self.store.set(key, value)


if __name__ == "__main__":
    server = Server("127.0.0.1", 5003, "127.0.0.1", 6003)
    server.start()
    # t =  Test(server)
    # t.start()
