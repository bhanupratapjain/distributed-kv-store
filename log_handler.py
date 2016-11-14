class LogHandler:
    def __init__(self,log_location):
        self.log_location = log_location
        self.log_index = 0
        self.log_commit_index = 0

    #check mismatch and append
    def append(self,key,val):
        if self.__check_mismatch() == True:
            raise Exception('sourabh there is an index mismatch!')
        index = self.get_recent_index() + 1

        with open(self.log_location, "a") as myfile:
            myfile.write(str(index)+ " "+key+" "+val+"\n")
        self.log_index = self.log_index+1

    #Not needed
    def get_log(self,index):
        fp = open(self.log_location)
        for i, line in enumerate(fp):
            if int(line.split(" ")[0]) == index:
                fp.close()
                return line
        return None

    def increase_commit_index(self):
        self.log_commit_index = self.log_commit_index + 1

    def __check_mismatch(self):
        return (self.log_commit_index != self.log_index)

    def get_recent(self):
        with open(self.log_location) as f:
            last = []
            for last in (line for line in f if line.rstrip('\n')):
                pass
        return last
    def get_recent_index(self):
        recent = self.get_recent()

        if len(recent) == 0:
            return 0
        else:
            return int(recent[0])

    def get_logs(self, start_index,end_index):
        lines = []
        print "index",start_index,end_index
        fp = open(self.log_location)
        for i, line in enumerate(fp):
            t = line.split(" ")
            if int(t[0]) < start_index or int(t[0])>end_index:
                pass
            else:
                lines.append(t)
        return lines

#if __name__ == "__main__":
#    l = LogHandler("store.log")
    #l.append("d","a")
    #    recent = l.get_recent()
    #print "recent log",recent[0],recent[1],recent[2]
    #print "get logs",l.get_logs(1,8)
    #print "get recent index", l.get_recent_index()
    #print "get log at index ", l.get_log(3)