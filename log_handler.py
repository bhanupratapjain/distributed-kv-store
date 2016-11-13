class LogHandler:
    def __init__(self,log_location):
        self.log_location = log_location
        self.log_index = 0
        self.log_commit_index = 0


    def append(self,key,val):
        with open(self.log_location, "a") as myfile:
            myfile.write(key+val)

    def get_log(self,index):
        fp = open(self.log_location)
        for i, line in enumerate(fp):
            if i == index:
                fp.close()
                return line

        return None


    def get_logs(self, start_index,end_index):
        pass

