import json
import socket
import threading


# Should Sync with other servers
# Register with LB
# Raise Exceptions
class Synchronizer:
    def __init__(self, client_address, server_address, file_handler, lb_address,
                 log_handler):
        self.lb_address = lb_address
        self.server_address = server_address
        self.file_handler = file_handler
        self.log_handler = log_handler
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.servers = []
        self.leader = None
        self.client_address = client_address

    # Setup Networking
    # Register With LB
    # Sync KeyStore from other server
    # Sets up socket to listen to other servers and LB for updates
    def start(self):
        self.__setup_socket()
        self.__register()
        self.__sync_keystore()
        t = threading.Thread(target=self.__listen)
        t.start()

    def __register(self):
        d = {"operation": "register", "server_ip": self.server_address[0],
             "server_port": self.server_address[1],
             "client_ip": self.client_address[0],
             "client_port": self.client_address[1]}

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(30)
        retries = 0
        while True:
            try:
                sock.sendto(json.dumps(d), self.lb_address)
                msg, addr = sock.recvfrom(1000)
                d = json.loads(msg)
                self.leader = (d['leader_ip'], d['leader_port'])
            except socket.timeout:
                retries += 1
                if retries == 3:
                    # Should Raise Exception
                    break

        sock.close()

    def __setup_socket(self):
        self.socket.bind(self.server_address)

    def __parser_server(self, d, addr):
        if d['operation'] == 'log':
            self.__append_log(d, addr)
        elif d['operation'] == 'commit':
            t = self.log_handler.get_recent()
            self.file_handler.set(t['key'], t['value'])
            self.log_handler.increase_commit_index()
        elif d['operation'] == 'sync':
            last_index = int(d['last_index'])
            logs = self.log_handler.get_logs(last_index + 1,
                                             self.log_handler.get_recent_index())
            ds = []
            for log in logs:
                d = {"index": log[0], "key": log[1], "val": log[2]}
                ds.append(d)
            self.socket.sendto(json.dumps(ds), addr)

    def __listen(self):
        while True:
            msg, addr = self.socket.recvfrom(1000)
            d = json.loads(msg)

            if addr == self.lb_address:
                self.__parse_lb(msg)
            else:
                self.__parser_server(d, addr)

    # TODO Update Leader
    def __parse_lb(self, msg):
        d = json.loads(msg)
        servers = []
        for server in d['servers']:
            ip = server['ip']
            port = server['port']
            servers.append((ip, port))
        self.servers = servers
        self.socket.sendto("Ok", self.lb_address)
        # self.leader = (d['leader']['ip'], d['leader']['port'])

    def __append_log(self, d, addr):
        try:
            if d['operation'] == 'set':
                self.log_handler.append(d['key'], d['value'])
                self.socket.sendto("Ok", addr)
        except IOError:
            print "append log failed %s" % addr
        except Exception:
            self.__sync_keystore()

    def __sync_keystore(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(30)

        # Fixing The Difference
        self.log_handler.log_index = self.log_handler.commit_index

        d = {"operation": "sync",
             "last_index": self.log_handler.get_recent_index()}
        sock.sendto(json.dumps(d), self.leader)
        logs = None
        js = ""
        while True:
            msg, addr = sock.recvfrom(1000)
            js += msg
            try:
                logs = json.loads(js)
                break
            except ValueError:
                pass

        for log in logs:
            self.log_handler.append(log['key'], log['val'])
            self.file_handler.set(log['key'], log['val'])
            self.log_handler.increase_commit_index()

        sock.close()

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
                print "server %s failed during  sync" % server
                msg = {'operation': 'remove', 'ip': server[0],
                       'port': server[1]}
                sock.sendto(json.dumps(msg), self.lb_address)

        if len(done) < 1:
            raise Exception("shutting down fail log")

        sock.close()

    def commit(self, key, value):
        d = {'operation': 'commit'}
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        for server in self.servers:
            sock.sendto(json.dumps(d), server)

        sock.close()


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(30)
    sock.recvfrom(1000)
