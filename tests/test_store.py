import multiprocessing
import time
from random import randint

from client import Client
from load_balancer import LoadBalancer
from request_parser import ProtoParser
from server import Server


class StoreTest:
    def __init__(self, store_location):
        self.store_location = store_location
        self.load_balancer = ()
        self.servers = []
        self.clients = []

    def __print_servers(self, srvs):
        for srv in srvs:
            self.__print_server(srv)

    def __print_server(self, srv):
        print "__________________________"
        print " CIP:{}, CPort:{}".format(srv['client_ip'], srv['client_port'])
        print " SIP:{}, SPort:{}".format(srv['server_ip'], srv['server_port'])

    def __add_new_lb(self, cip, cport, sip, sport):
        p = multiprocessing.current_process()
        lb = LoadBalancer(cip, cport, sip, sport)
        print "****[Adding Load Balancer [{}]]".format(p.pid)
        # print " CIP:{}, CPort:{}".format(lb.cip, lb.cport)
        # print " SIP:{}, SPort:{}".format(lb.sip, lb.sport)
        # print "-------------------------------------"
        lb.start()
        # while 1:
        # print "\n\n================Load Balancer Stats [{}]================".format(p.pid)
        # print " CIP:{}, CPort:{}".format(lb.cip, lb.cport)
        # print " SIP:{}, SPort:{}".format(lb.sip, lb.sport)
        # print "\n---------------Leader-------------------"
        # if lb.leader is not None:
        #     self.__print_server(lb.leader)
        # else:
        #     print "No Leader Elected"
        # print "\n---------------Followers--------------"
        # if len(lb.followers) < 1:
        #     print "No Followers"
        # else:
        #     self.__print_servers(lb.followers)
        # print "\n================================================================\n\n"
        # time.sleep(5)

    def __add_new_server(self, cip, cport, sip, sport, lbip, lbport):
        p = multiprocessing.current_process()
        srv = Server(cip, cport, sip, sport, lbip, lbport)
        print "****[Adding Server[{}]]".format(p.pid)
        # print " CIP:{}, CPort:{}".format(srv.cip, srv.cport)
        # print " SIP:{}, SPort:{}".format(srv.sip, srv.sport)
        # print " LIP:{}, LPort:{}".format(srv.lbip, srv.lbport)
        # print "-------------------------------------"
        srv.start()

    def __add_new_client(self, cip, cport, lbip, lbport):
        client = Client(cip, cport)
        server_addr = ProtoParser.parse_srv_addr(
            client.get_server(lbip, lbport))
        print "server ", server_addr
        client.set("hello", "1", server_addr[0], int(server_addr[1]))
        print "get result, ", client.get("hello", server_addr[0],
                                         int(server_addr[1]))

    def __add_new_client_with_random(self, cip, cport, lbip, lbport):
        client = Client()
        server_addr =  client.get_server(lbip, lbport)
        print "server ", server_addr
        for i in xrange(0, 500):
            print "Round [{}] for client [{}]".format(i, cport)
            key = str(randint(0, 1000))
            client.set(str(randint(0, 1000)), str(randint(0, 1000)), server_addr[0],server_addr[1])
            print "get result, ", key, client.get((key,randint(0,1000)), server_addr[0],server_addr[1])

    # Happy Case
    # 1. Add Load Balancer
    # 2. Add Servers
    # 3. No Kill
    def test_case_1(self, lb, servers, clients):
        lb_p = multiprocessing.Process(target=self.__add_new_lb,
                                       args=(
                                           lb[0][0], lb[0][1], lb[1][0],
                                           lb[1][1]),
                                       name='load_balancer')
        lb_p.start()
        self.load_balancer = lb_p
        time.sleep(2)

        for i, srv in enumerate(servers):
            srv_p = multiprocessing.Process(target=self.__add_new_server,
                                            args=(srv[0][0],
                                                  srv[0][1],
                                                  srv[1][0],
                                                  srv[1][1],
                                                  srv[2][0],
                                                  srv[2][1]),
                                            name='server')
            srv_p.start()
            self.servers.append(srv_p)
            time.sleep(1)

        time.sleep(2)
        for client in clients:
            client_p = multiprocessing.Process(target=self.__add_new_client,
                                               args=(client[0],
                                                     client[1],
                                                     lb[0][0],
                                                     lb[0][1]),
                                               name='client')
            client_p.start()
            self.clients.append(client_p)
            time.sleep(2)

        self.load_balancer.join()
        for srv_p in self.servers:
            srv_p.join()
        for cli_p in self.clients:
            cli_p.join()

    # 1. 1 LB
    # 2. 4 Server
    # 3. 4 clients
    # 4. Random set/get for 100 run
    def test_case_2(self, lb, servers, client):
        lb_p = multiprocessing.Process(target=self.__add_new_lb,
                                       args=(
                                           lb[0][0], lb[0][1], lb[1][0],
                                           lb[1][1]),
                                       name='load_balancer')
        lb_p.start()
        self.load_balancer = lb_p
        time.sleep(2)

        for i, srv in enumerate(servers):
            srv_p = multiprocessing.Process(target=self.__add_new_server,
                                            args=(srv[0][0],
                                                  srv[0][1],
                                                  srv[1][0],
                                                  srv[1][1],
                                                  srv[2][0],
                                                  srv[2][1]),
                                            name='server')
            srv_p.start()
            self.servers.append(srv_p)
            time.sleep(1)

        time.sleep(2)
        for client in clients:
            client_p = multiprocessing.Process(
                target=self.__add_new_client_with_random,
                args=(client[0],
                      client[1],
                      lb[0][0],
                      lb[0][1]),
                name='client')
            client_p.start()
            self.clients.append(client_p)
            time.sleep(2)

        self.load_balancer.join()
        for srv_p in self.servers:
            srv_p.join()
        for cli_p in self.clients:
            cli_p.join()

    def __add_new_test_server(self, i):
        srv_p = multiprocessing.Process(target=self.__add_new_server,
                                        args=(servers[i][0][0],
                                              servers[i][0][1],
                                              servers[i][1][0],
                                              servers[i][1][1],
                                              servers[i][2][0],
                                              servers[i][2][1]),
                                        name='server')
        srv_p.start()
        self.servers.append(srv_p)

    def test_case_3(self, lb, servers, client):
        lb_p = multiprocessing.Process(target=self.__add_new_lb,
                                       args=(
                                           lb[0][0], lb[0][1], lb[1][0],
                                           lb[1][1]),
                                       name='load_balancer')
        lb_p.start()
        self.load_balancer = lb_p
        time.sleep(2)

        for i, srv in enumerate(servers):
            srv_p = multiprocessing.Process(target=self.__add_new_server,
                                            args=(srv[0][0],
                                                  srv[0][1],
                                                  srv[1][0],
                                                  srv[1][1],
                                                  srv[2][0],
                                                  srv[2][1]),
                                            name='server')
            srv_p.start()
            self.servers.append(srv_p)
            time.sleep(1)

        time.sleep(2)

        killed = False

        # for i, client in enumerate(clients):
        #     client_p = multiprocessing.Process(
        #         target=self.__add_new_client_with_random,
        #         args=(client[0],
        #               client[1],
        #               lb[0][0],
        #               lb[0][1]),
        #         name='client')
        #     client_p.start()
        #     self.clients.append(client_p)
            # if i == 3:
            #     self.servers.pop(4).terminate()
            #     print "Killed Server"
            #     time.sleep(10)
            #     print "Continue Creating Clients"
            #     threading.Timer(5, self.__add_new_test_server, args=(4,)).start()

            # time.sleep(2)

        self.load_balancer.join()

        for srv_p in self.servers:
            srv_p.join()
        for cli_p in self.clients:
            cli_p.join()


if __name__ == "__main__":
    st = StoreTest("/test_data")
    lb = (('127.0.0.1', 5020), ('127.0.0.1', 5022))
    servers = [
        (('127.0.0.1', 6001), ('127.0.0.1', 6002), lb[1]),
        (('127.0.0.1', 6003), ('127.0.0.1', 6004), lb[1]),
        (('127.0.0.1', 6005), ('127.0.0.1', 6006), lb[1]),
        (('127.0.0.1', 6007), ('127.0.0.1', 6008), lb[1]),
        (('127.0.0.1', 6009), ('127.0.0.1', 6010), lb[1]),
        (('127.0.0.1', 6011), ('127.0.0.1', 6012), lb[1]),
        (('127.0.0.1', 6013), ('127.0.0.1', 6014), lb[1]),
        (('127.0.0.1', 6015), ('127.0.0.1', 6016), lb[1]),
        (('127.0.0.1', 6017), ('127.0.0.1', 6018), lb[1]),
        (('127.0.0.1', 6019), ('127.0.0.1', 6020), lb[1]),
    ]
    clients = [
        ('127.0.0.1', 7001),
        ('127.0.0.1', 7002),
        ('127.0.0.1', 7003),
        ('127.0.0.1', 7004),
        ('127.0.0.1', 7005),
        ('127.0.0.1', 7006),
        ('127.0.0.1', 7007),
        ('127.0.0.1', 7008),
        ('127.0.0.1', 7009),
        ('127.0.0.1', 7010),
    ]
    st.test_case_3(lb, servers, clients)
    # st.test_case_2(lb, servers, clients)
