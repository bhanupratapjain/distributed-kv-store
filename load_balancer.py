# Accept Registrations
# Round Robin Returning of Servers
# Should push updated servers list to servers
# Extension Poll Servers for Fault Tolerance


class LoadBalancer:
    def __init__(self, ip, port):
        self.servers = []
        self.ip = ip
        self.port = port

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
