# Gets or Sets to the file should use locks and raise exceptions

import threading
from shutil import move
from tempfile import mkstemp

from os import remove, close


# import portalocker
class FileHandler:
    def __init__(self, store_location):

        # File Object for store
        self.store_file = store_location
        self.__init_files()
        self.data = None

    def __init_files(self):
        open(self.store_file, 'a')

    # Searches File and Returns
    def get(self, key):
        fp = open(self.store_file, 'r')
        for line in fp:
            if line.split()[0] == key:
                fp.close()
                return line.split()[1]
        return None

    # Appends/Overwrites Key,Value in File
    # If Value is None then deletes the Key
    def set(self, key, value):
        key_found = False
        fh, new_file = mkstemp()
        with open(new_file, 'w') as nf:
            with open(self.store_file) as f:
                for line in f:
                    t = line.split()
                    if t[0] == key:
                        key_found = True
                        line = t[0] + " " + value + "\n"
                    if value is not None:
                        nf.write(line)
        close(fh)
        remove(self.store_file)
        move(new_file, self.store_file)
        if not key_found and value is not None:
            with open(self.store_file, "a") as myfile:
                myfile.write(key + " " + value + "\n")


"""
if __name__ == "__main__":
    f = FileHandler("keys.txt")
    t = Test(f)
    t.start()
    f.set("4","f2")
    print f.get("4")
    f.set("4", "f3")
    print f.get("4")
    print f.get("asjfdhaskj")
"""