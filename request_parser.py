class ProtoParser:
    def __init__(self):
        print ""

    # Returns tuple of (op, key, value)
    @staticmethod
    def parse(msg):
        t = msg.strip().split(" ")
        if t[0] == "get":
            return [t[0], t[1]]
        elif t[0] == "get-servers":
            return [t[0]]
        else:
            ret_val = [t[0], t[1], t[4]]
            return ret_val

    @staticmethod
    def parse_set(msg):
        lines = msg.split("\r\n")
        line1 = lines[0].split(" ")
        line2 = lines[1].split(" ")
        return [line1[0], line1[1], line2[0]]

    @staticmethod
    def parse_srv_addr(msg):
        lines = msg.split("\r\n")
        return lines[0].split(":")
