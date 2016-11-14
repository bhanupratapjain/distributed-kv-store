# Accept Registrations
# Round Robin Returning of Servers
# Should push updated servers list to servers
# Extension Poll Servers for Fault Tolerance
import socket, threading
import json
from random import randint

HEART_BEAT = 30


class ClientThread(threading.Thread):
    def __init__(self, ip, port, socket, leader):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket
        self.leader = leader
        print "[+] New thread started for %s:%s" % (ip, port)

    def __parse(self, msg):
        pass

    def run(self):
        msg = self.socket.recv(1000)
        print msg
        if self.__parse(msg) == "get-servers":
            resp = self.leader['client_ip'] + ":" + self.leader["clienet_port"] + "\r\nend\r\n"
            self.socket.sendall(resp)


class ServerThread(threading.Thread):
    def __init__(self, ip, port, socket, msg, followers, leader):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.msg = msg
        self.leader = leader
        self.followers = followers
        self.socket = socket
        print "[+] New thread started for %s:%s" % (ip, port)

    def __get_leader_addr(self):
        if self.leader in None:
            self.leader = self.followers[0]
        return self.leader['server_ip'], self.leader['server_port']

    def __register_server(self, client_ip, client_port, server_ip, server_port):
        # STEP 1: Add the server to the server list.
        if self.leader is not None:
            self.followers.append({
                "client_ip": client_ip,
                "client_port": client_port,
                "server_ip": server_ip,
                "server_port": server_port,
                "leader": False
            })
        # STEP 2: Send leader info back to the server.
        leader_addr = self.__get_leader_addr()
        data = {"operation": "register_callback", "leader_ip": leader_addr[0], "leader_port": leader_addr[1]}
        self.socket.sentto(data, (self.ip, self.port))

    def __process_server_request(self, msg):
        if 'operation' in msg and msg['operation'] == 'register':
            client_ip = msg['client_ip']
            client_port = msg['client_port']
            server_ip = msg['server_ip']
            server_port = msg['server_port']
            self.__register_server(client_ip, client_port, server_ip, server_port)

    def run(self):
        self.__process_server_request(json.dumps(self.msg))

        pass


class LoadBalancer:
    def __init__(self, ip, port):
        self.followers = []
        self.leader = None
        self.ip = ip
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __setup_client_socket(self):
        self.socket.bind((self.ip, self.port))

    def __setup_server_socket(self):
        self.socket.bind((self.ip, self.port))

    def __listen_server(self):
        while 1:
            (msg, (ip, port)) = self.server_socket.recvfrom(1000)
            th = ServerThread(ip, port, msg, self.server_socket, self.followers, self.leader)
            th.run()

    def __listen_client(self):
        self.socket.listen(50)
        while 1:
            (rec_socket, (ip, port)) = self.socket.accept()
            th = ClientThread(ip, port, rec_socket, self.leader)
            th.run()

    def start(self):
        self.__setup_client_socket()
        self.__setup_server_socket()
        client_socket_thread = threading.Thread(target=self.__listen_client)
        server_socket_thread = threading.Thread(target=self.__listen_server)
        client_socket_thread.start()
        server_socket_thread.start()
        # Create a heartbeat thread every 30 sec.
        threading.Timer(HEART_BEAT, self.__heart_beat).start()

    # TODO Fix Timer by looping with wait
    def __heart_beat(self):
        if self.leader is None:
            self.__elect_leader()

        local_followers = []
        for follower in self.followers:
            local_followers.append({
                "ip": follower["server_ip"],
                "port": follower["server_port"]
            })

        # Check for leader heartbeat and update server list.
        data = {"operation": "heartbeat", "servers": local_followers}
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(30)
        try:
            sock.sendto(json.dumps(data), (self.leader['server_ip'], self.leader['server_port']))
            msg, addr = sock.recvfrom(1000)
            if msg == 'ok':
                pass
        except socket.timeout:
            self.__elect_leader()
            self.__heart_beat()
        sock.close()

    def __elect_leader(self):
        self.leader = self.followers.pop(randint(0, len(self.followers)))

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
