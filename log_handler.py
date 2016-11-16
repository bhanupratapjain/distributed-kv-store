# TODO log_index default is 0 or else
# TODO delete last log index row by default
import threading


class LogHandler:
    def __init__(self, log_location):
        self.lock = threading.Lock()
        self.log_location = log_location
        self.__init_files()
        self.log_index = self.get_recent_index()
        self.log_commit_index = self.get_recent_index()

    def __init_files(self):
        with self.lock:
            open(self.log_location, 'a').close()
            self.delete_last_line()

    # check mismatch and append
    def append(self, key, val):
        with self.lock:
            if self.__check_mismatch():
                raise Exception('there is an index mismatch!')
            index = self.log_index + 1
            with open(self.log_location, "a") as myfile:
                myfile.write(str(index) + " " + key + " " + val + "\n")
                myfile.flush()
            self.log_index += 1

    # Not needed
    def get_log(self, index):
        with self.lock:
            fp = open(self.log_location, 'r')
            for i, line in enumerate(fp):
                if int(line.split()[0]) == index:
                    fp.close()
                    return line
            return None

    def increase_commit_index(self):
        with self.lock:
            self.log_commit_index += 1

    def __check_mismatch(self):
        return self.log_commit_index != self.log_index

    def get_recent(self):
        with self.lock:
            with open(self.log_location, 'r') as f:
                last = ""
                for last in (line for line in f if line.rstrip('\n')):
                    pass
            return last.split()

    def get_recent_index(self):
        r = self.get_recent()
        if len(r) == 0:
            return 0
        else:
            return int(r[0])

    def get_logs(self, start_index, end_index):
        lines = []
        with self.lock:
            fp = open(self.log_location, 'r')
            for line in fp:
                t = line.split()
                if int(t[0]) < start_index or int(t[0]) > end_index:
                    pass
                else:
                    lines.append(t)
            return lines

    def delete_last_line(self):
        f = open(self.log_location, 'rb')
        pos = n = 0
        for line in f:
            pos = n
            n += len(line)
        f = open(self.log_location, 'ab')
        f.truncate(pos)


"""
if __name__ == "__main__":
    l = LogHandler("store.log")
    t = TestLog(l)
    t.start()

    #l.append("s", "a")
    #l.increase_commit_index()
    #l.append("a", "a")
    #l.increase_commit_index()
    #l.append("d", "a")
    #l.increase_commit_index()

    recent = l.get_recent()
    print "recent log", recent
    print "get logs", l.get_logs(1, 8)
    print "get recent index", l.get_recent_index()
    print "get log at index ", l.get_log(3)
"""

