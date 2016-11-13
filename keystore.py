# Sets to File and sync to other servers
# Gets from File
class KeyStore:
    def __init__(self):
        self.file_handler = None
        self.synchronizer = None

    # Setup File Handler and Synchronzier
    def start(self, lb_address):
        pass

    # Returns Value or None if not found
    # Raises exception if any other error
    def get(self, key):
        pass

    # Doesnt Return Anything
    # Raises exception if any error (Exception Class)
    def set(self, key, value):
        pass
