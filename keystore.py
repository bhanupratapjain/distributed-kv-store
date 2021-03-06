import threading

from file_handler import FileHandler
from log_handler import LogHandler
from synchronizer import Synchronizer


# Sets to File and sync to other servers
# Gets from File
class KeyStore:
    def __init__(self, lb_address, client_address, server_address):
        self.server_address = server_address
        self.file_handler = FileHandler(
            "keys_" + str(server_address[1]) + ".txt")
        self.log_handler = LogHandler(
            "store_" + str(server_address[1]) + ".log")
        self.synchronizer = Synchronizer(client_address, server_address,
                                         self.file_handler,
                                         lb_address,
                                         self.log_handler)
        self.lock = threading.Lock()

    # Setup File Handler and Synchronzier
    def start(self):
        self.synchronizer.start()

    # Returns Value or None if not found
    # Raises exception if any other error
    def get(self, key):
        with self.lock:
            return self.file_handler.get(key)

    # Doesnt Return Anything
    # Raises exception if any error (Exception Class)
    def set(self, key, value):
        with self.lock:
            # Appends Log
            # print "Acquired Lock By Thread", self.server_address
            self.log_handler.append(key, value)

            # Syncs Log across servers
            self.synchronizer.sync_log(key, value)

            # Sets Key in File
            self.file_handler.set(key, value)

            # Increase the commit index
            self.log_handler.increase_commit_index()

            # Commits on all servers
            self.synchronizer.commit(key, value)

        # print "Released Lock By Thread", self.server_address
