# Accept Registrations
# Round Robin Returning of Servers
# Should push updated servers list to servers
# Extension Poll Servers for Fault Tolerance
import socket,threading


class ClientThread(threading.Thread):

    def __init__(self, ip, port, socket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket
        print "[+] New thread started for "+ip+":"+str(port)

    def run(self):
        msg = clientsocket.recv(1000)
        parts = msg.split()
        print msg
        if parts[0] == "set":
            self.set(parts[1], parts[2])
            clientsocket.send("Done")
        else:
            value = self.get(parts[1])
            clientsocket.send(value)

class LoadBalancer:
    def __init__(self, ip, port):
        self.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.servers = []
        self.ip = ip
        self.port = port


    def send(self):
        pass

    def recv(self,client_socket):
        pass


    def start(self):
        self.socket.bind((self.ip, self.port))
        self.socket.listen(5)
        while 1:
            (clientsock, (ip, port)) = self.socket.accept()
            # ct = client_thread(clientsocket)
            # ct.run()
            ct= ClientThread(ip, port, clientsock)
            ct.run()

    def add_sever(self, ip, port):
        # STEP 1: Verify Server
        # STEP 2: Add server to server pool
        # STEP 3: Broadcast Server Pool.
        pass

    def remove_server(self, ip, port):
        # STEP 1: Verify no active connections on the server to be removed
        # STEP 2: Remove server to server pool
        # STEP 3: Broadcast Updated Server Pool.
        pass

    def get_server_info(self, ip, port):
        # STEP 1: Get server info from the requested server.
        pass

    def get_servers(self):
        # STEP 1: Return the server with least no. of active connections.
        pass


if __name__ == "__main__":
    pass
