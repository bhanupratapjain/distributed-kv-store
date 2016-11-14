# Gets or Sets to the file should use locks and raise exceptions

import json


class FileHandler:
    def __init__(self, store_location):
        # TODO Preferably Read Write Lock (Only 1 Writer, but any number of readers)
        self.lock = None
        # File Object for store
        self.store_file = store_location
        self.data = None

    # Searches File and Returns
    # TODO Handle Key Error
    def get(self, key):
        self.update_data()
        return self.data[key]

    # Appends/Overwrites Key,Value in File
    # If Value is None then deletes the Key
    def set(self, key, value):
        # save to file:
        self.update_data()
        with open(self.store_file, 'w') as f:
            self.data[key] = value
            json.dump(self.data, f)

    def update_data(self):
        # load from file:
        with open(self.store_file, 'r') as f:
            try:
                self.data = json.load(f)
            except ValueError:
                self.data = {}
