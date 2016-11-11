# Should Sync with other servers
# Register with LB
# Raise Exceptions
class Synchronizer:
    def __init__(self, file_handler, lb_address):
        self.socket = None
        self.servers = []

    # Setup Networking
    # Register With LB
    # Sync KeyStore from other server
    # Sets up socket to listen to other servers and LB for updates
    def start(self):
        pass

    # Syncs the set with all Servers
    # Should be reliable like if one fails all else should reverted
    def sync_set(self, key, value):
        pass
