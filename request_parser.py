class ProtoParser:
    def __init__(self):
        print ""

    # Returns tuple of (op, key, value)
    @staticmethod
    def parse(msg):
        t = msg.split(" ")
        if(t[0] == "get"):
            return [t[0],t[1]]
        else:
            ret_val = [t[0],t[1],t[4]]
            return ret_val

