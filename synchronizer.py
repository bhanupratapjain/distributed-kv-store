import json
import socket
import threading


# Should Sync with other servers
# Register with LB
# Raise Exceptions
class Synchronizer:
    def __init__(self, file_handler, lb_address,log_handler):
        self.lb_address = lb_address
        self.file_handler = file_handler
        self.log_handler = log_handler
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.servers = []
        self.address = None

    # Setup Networking
    # Register With LB
    # Sync KeyStore from other server
    # Sets up socket to listen to other servers and LB for updates
    def start(self, address):
        self.address = ("127.0.0.1", 5001)
        self.__setup_socket()
        self.__register()
        self.__sync_keystore()
        t = threading.Thread(target=self.__listen)
        t.start()

    def __register(self):
        pass

    def __setup_socket(self):
        self.socket.bind(self.address)

    def __parser_server(self,d,addr):
        if d['operation'] == 'log':
            self.__append_log(d, addr)
        elif d['operation'] == 'commit':
            self.file_handler.set(d['key'], d['value'])

    def __listen(self):
        while True:
            msg, addr = self.socket.recvfrom(1000)
            d = json.loads(msg)


            if addr == self.lb_address:
                self.servers = self.__parse_lb(msg)
            else:
                self.__parser_server(d,addr)

    def __parse_lb(self, msg):
        pass

    def __append_log(self, d, addr):
        try:
            if d['operation'] == 'set':
                #self.file_handler.set(d['key'], d['value'])
                self.log_handler.append(d['key'], d['value'])
                self.socket.sendto("Ok", addr)
        except Exception:
            self.socket.sendto("Reject", addr)

    def __sync_keystore(self):
        pass

    # Syncs the set with all Servers
    # Should be reliable like if one fails all else should reverted
    # Issue if the server crashes here when incomplete as entire system will be
    # in inconsistent state
    def sync_log(self, key, value):
        d = {'operation': 'log', 'key': key, 'value': value}
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(30)
        done = []

        for server in self.servers:
            try:
                sock.sendto(json.dumps(d), server)
                msg, addr = sock.recvfrom(1000)
                if msg == 'Ok':
                    done.append(server)
            except socket.timeout:
                #TODO
                #tell load balancer which server failed remove from this server list also
                print "server %s failed during  sync" % server

        if len(done) < 1:
            raise Exception("shutting down fail log")

                #We dont need this
                #d = {'operation': 'undo_log'}
                #for server in done:
                #    sock.sendto(json.dumps(d), server)

        sock.close()


    def commit_log(self, key, value):
        d = {'operation': 'commit'}
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(30)
        done = []

        for server in self.servers:
            try:
                sock.sendto(json.dumps(d), server)
                msg, addr = sock.recvfrom(1000)
                if msg == 'Ok':
                    done.append(server)
            except socket.timeout:
                # TODO
                # tell load balancer which server failed remove from this server list also
                print "server %s failed during commit"%server
        if len(done) < 1:
            raise Exception("shutting down Fail commit")
        # We dont need this
        # d = {'operation': 'undo_log'}
        # for server in done:
        #    sock.sendto(json.dumps(d), server)

        sock.close()

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(30)
    sock.recvfrom(1000)
