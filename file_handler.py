# Gets or Sets to the file should use locks and raise exceptions
class FileHandler:
    def __init__(self, store_location):
        # Preferably Read Write Lock (Only 1 Writer, but any number of readers)
        self.lock = None
        # File Object for store
        self.store_file = None

        # Searches File and Returns
        def get(self, key):
            pass

        # Appends/Overwrites Key,Value in File
        # If Value is None then deletes the Key
        def set(self, key, value):
            pass
