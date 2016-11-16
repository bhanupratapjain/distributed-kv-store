# Accept Registrations
# Round Robin Returning of Servers
# Should push updated servers list to servers
# Extension Poll Servers for Fault Tolerance
import json
import socket
import threading
import time
from random import randint
from constants import HEART_BEAT
import constants
from request_parser import ProtoParser




class LoadBalancer:
    def __init__(self, cip, cport, sip, sport):
        self.followers = []
        self.lock = threading.Lock()
        self.leader = None
        self.cip = cip
        self.cport = cport
        self.sip = sip
        self.sport = sport
        self.server_socket = socket.socket(socket.AF_INET,
                                           socket.SOCK_DGRAM)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __setup_client_socket(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.cip, self.cport))

    def __setup_server_socket(self):
        self.server_socket.bind((self.sip, self.sport))

    def __listen_server(self):
        while True:
            (msg, (ip, port)) = self.server_socket.recvfrom(constants.BUFFER_SIZE)
            threading.Thread(target=self.__process_server_request,
                             args=(json.loads(msg), (ip, port))).start()

    def __listen_client(self):
        self.socket.listen(constants.LOAD_BALANCER_QUEUE_SIZE)
        while True:
            (rec_socket, (ip, port)) = self.socket.accept()
            # print "got client req"
            threading.Thread(target=self.__process_client_request,
                             args=(ip, port, rec_socket,)).start()

    def __process_client_request(self, cip, cport, client_sock):
        msg = client_sock.recv(constants.BUFFER_SIZE)
        #parsed_msg = ProtoParser.parse(msg)
        parsed_msg = ProtoParser.parse_block(msg)
        operation = parsed_msg.iterkeys().next()
        if operation == "get-servers":
            resp = self.leader['client_ip'] + ":" + str(
                self.leader["client_port"]) + "\r\nend\r\n"
            client_sock.sendall(resp)

    def __get_leader_addr(self):
        return self.leader['server_ip'], self.leader['server_port']

    def __register_server(self, client_ip, client_port, server_ip, server_port,
                          ret_ip, ret_port):
        # STEP 1: Add the server to the server list.
        if self.leader is not None:
            self.followers.append({
                "client_ip": client_ip,
                "client_port": client_port,
                "server_ip": server_ip,
                "server_port": server_port,
                "leader": False
            })
        else:
            self.leader = {"client_ip": client_ip, "client_port": client_port,
                           "server_ip": server_ip, "server_port": server_port,
                           "leader": True}
        # STEP 2: Send leader info back to the server.
        leader_addr = self.__get_leader_addr()
        data = {"operation": "register_callback",
                "leader_ip": leader_addr[0], "leader_port": leader_addr[1]}
        self.server_socket.sendto(json.dumps(data), (ret_ip, ret_port))

    def __process_server_request(self, msg, rec_sock_addr):
        if 'operation' in msg and msg['operation'] == 'register':
            # print "Got server registration req"
            # print msg
            client_ip = msg['client_ip']
            client_port = msg['client_port']
            server_ip = msg['server_ip']
            server_port = msg['server_port']
            with self.lock:
                self.__register_server(client_ip, client_port, server_ip,
                                       server_port, rec_sock_addr[0],
                                       rec_sock_addr[1])
        elif msg['operation'] == 'remove':
            server_ip = msg['server_ip']
            server_port = msg['server_port']
            index = 0
            for i, follower in enumerate(self.followers):
                if follower['server_ip'] == server_ip and follower[
                    'server_port'] == server_port:
                    index = i
                    break

            self.followers.pop(index)

    def start(self):
        self.__setup_client_socket()
        self.__setup_server_socket()
        client_socket_thread = threading.Thread(target=self.__listen_client)
        server_socket_thread = threading.Thread(target=self.__listen_server)
        client_socket_thread.start()
        server_socket_thread.start()
        # Create a heartbeat thread every 30 sec.
        threading.Thread(target=self.__heart_beat).start()
        client_socket_thread.join()
        server_socket_thread.join()

    def __heart_beat(self):
        while True:
            # print "\n#########lb HB, leader is"
            if self.leader is None:
                self.__elect_leader()
                time.sleep(HEART_BEAT)
                continue

            local_followers = []
            for follower in self.followers:
                local_followers.append({
                    "ip": follower["server_ip"],
                    "port": follower["server_port"]
                })

            # Check for leader heartbeat and update server list.
            data = {"operation": "heartbeat", "servers": local_followers}
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(constants.SOCKET_TIMEOUT)
            try:
                sock.sendto(json.dumps(data), (
                    self.leader['server_ip'], self.leader['server_port']))
                msg, addr = sock.recvfrom(constants.BUFFER_SIZE)
                if msg == 'ok':
                    print "alive" #self.leader['server_port'], self.followers
                    time.sleep(HEART_BEAT)
            except socket.timeout:
                print "dead"
                self.__elect_leader()
            sock.close()

    def __elect_leader(self):
        if len(self.followers) < 1:
            return
        current_followers = []
        data = {"operation": "heartbeat", "servers": []}
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for follower in self.followers:
            sock.sendto(json.dumps(data),
                        (follower['server_ip'], follower['server_port']))
            msg, addr = sock.recvfrom(constants.BUFFER_SIZE)
            if msg == "ok":
                current_followers.append(follower)
        with self.lock:
            self.followers = current_followers
            self.leader = self.followers.pop(
                randint(0, len(self.followers) - 1))

    def get_server_info(self, ip, port):
        # STEP 1: Get server info from the requested server.
        pass

    def get_servers(self):
        # STEP 1: Return the server with least no. of active connections.
        pass


if __name__ == "__main__":
    lb = LoadBalancer('127.0.0.1', 4500, "127.0.0.1", 4501)
    lb.start()
