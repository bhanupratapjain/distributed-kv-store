class LogHandler:
    def __init__(self, log_location):
        self.log_location = log_location
        self.log_index = 0
        self.log_commit_index = 0

    def append(self, key, val):
        pass

    def get_log(self, index):
        pass

    def get_logs(self, start_index, end_index):
        pass
