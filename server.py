import socket
from keystore import KeyStore


class Server:
    def __init__(self, address,port , lb_address):
        # create an INET, STREAMing socket
        self.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.ip = address
        self.port = port
        #self.store = dict()  # KeyStore
        self.store = KeyStore()  # KeyStore

    def start(self):
        self.socket.bind((self.ip, self.port))
        self.socket.listen(5)
        while 1:
            (clientsocket, address) = self.socket.accept()
            # ct = client_thread(clientsocket)
            # ct.run()
            msg = clientsocket.recv(1000)
            parts = msg.split()
            #ProtoParser.parse()
            print msg
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
        self.store.set(key,value)


if __name__ == "__main__":
    server = Server("127.0.0.1", 5001,"127.0.0.1")
    server.start()
