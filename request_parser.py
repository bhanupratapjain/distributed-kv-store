class ProtoParser:
    def __init__(self):
        print ""

    # Returns tuple of (op, key, value)
    @staticmethod
    def parse(msg):
        return msg.split(" ")

