# TODO log_index default is 0 or else
# TODO delete last log index row by default
class LogHandler:
    def __init__(self, log_location):
        self.log_location = log_location
        self.log_index = self.get_recent_index()
        self.log_commit_index = self.get_recent_index()

    # check mismatch and append
    def append(self, key, val):
        if self.__check_mismatch():
            raise Exception('there is an index mismatch!')
        index = self.log_index + 1

        with open(self.log_location, "a") as myfile:
            myfile.write(str(index) + " " + key + " " + val + "\n")
            myfile.flush()
        self.log_index += 1

    # Not needed
    def get_log(self, index):
        fp = open(self.log_location, 'r')
        for i, line in enumerate(fp):
            if int(line.split(" ")[0]) == index:
                fp.close()
                return line
        return None

    def increase_commit_index(self):
        self.log_commit_index += 1

    def __check_mismatch(self):
        return self.log_commit_index != self.log_index

    def get_recent(self):
        with open(self.log_location, 'r') as f:
            last = []
            for last in (line for line in f if line.rstrip('\n')):
                pass
        return last

    # TODO Replace with old code
    def get_recent_index(self):
        return self.log_index

    def get_logs(self, start_index, end_index):
        lines = []
        fp = open(self.log_location, 'r')
        for line in fp:
            t = line.split(" ")
            if int(t[0]) < start_index or int(t[0]) > end_index:
                pass
            else:
                lines.append(t)
        return lines


if __name__ == "__main__":
    l = LogHandler("store.log")
    l.append("d", "a")
    l.append("d", "a")
    l.append("d", "a")
    recent = l.get_recent()
    print "recent log", recent[0], recent[1], recent[2]
    print "get logs", l.get_logs(1, 8)
    print "get recent index", l.get_recent_index()
    print "get log at index ", l.get_log(3)
