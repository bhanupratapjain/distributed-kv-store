from file_handler import FileHandler
# Sets to File and sync to other servers
# Gets from File
class KeyStore:
    def __init__(self):
        self.file_handler = FileHandler("keys.json")
        self.synchronizer = None

    # Setup File Handler and Synchronzier
    def start(self, lb_address):
        pass

    # Returns Value or None if not found
    # Raises exception if any other error
    def get(self, key):
        return self.file_handler.get(key)

    # Doesnt Return Anything
    # Raises exception if any error (Exception Class)
    def set(self, key, value):
        self.file_handler.set(key, value)
