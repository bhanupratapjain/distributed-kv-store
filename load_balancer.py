# Accept Registrations
# Round Robin Returning of Servers
# Should push updated servers list to servers
# Extension Poll Servers for Fault Tolerance
import multiprocessing
import socket


class LoadBalancer:
    def __init__(self, ip, port):
        self.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.servers = []
        self.ip = ip
        self.port = port

    def start(self):
        self.socket.bind((self.ip, self.port))
        self.socket.listen(5)
        while 1:
            (clientsocket, address) = self.socket.accept()
            # ct = client_thread(clientsocket)
            # ct.run()
            msg = clientsocket.recv(1000)
            parts = msg.split()
            print msg
            if parts[0] == "set":
                self.set(parts[1], parts[2])
                clientsocket.send("Done")
            else:
                value = self.get(parts[1])
                clientsocket.send(value)

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
