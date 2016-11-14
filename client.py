import socket


class Client:
    def __init__(self, ip, port, sip, sport):
        self.ip = ip
        self.port = port
        self.sip = sip
        self.sport = sport

        # create an INET, STREAMing socket

        # now connect to the web server on port 80
        # - the normal http port

    def get(self, key):
        self.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.sip, self.sport))
        self.socket.send("get " + key)
        msg = self.socket.recv(1000)
        print msg

    def set(self, key, value):
        self.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.sip, self.sport))
        self.socket.send("set " + key + " " + value)
        msg = self.socket.recv(1000)
        print msg


if __name__ == "__main__":
    client = Client("127.0.0.1", 6003, "127.0.0.1", 5003)
    client.set("as", "2000")
    client.get("as")
