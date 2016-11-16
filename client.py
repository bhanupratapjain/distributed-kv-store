import socket


class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def get(self, key, sip, sport):
        sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((sip, sport))
        sock.send("get " + key + "\r\n")
        msg = sock.recv(1000)
        sock.close()
        return msg

    def set(self, key, value, sip, sport):
        sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((sip, sport))
        sock.send("set " + key + " 0 0 " + value + " [noreply]\r\n")
        msg = sock.recv(1000)
        print msg
        sock.close()

    def get_server(self, sip, sport):
        print "creating scoket", sip, sport
        sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((sip, sport))
        sock.send("get-servers")
        msg = sock.recv(1000)
        # print msg
        sock.close()
        return msg

# if __name__ == "__main__":
#
# client = Client("127.0.0.1", 6003, "127.0.0.1", 5003)
# client.set("as", "2000")
# client.get("as")
