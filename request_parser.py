class ProtoParser:
    def __init__(self):
        print ""


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
    # Returns tuple of (op, key, value)
    @staticmethod
    def parse_block(st):
        msgs = st.strip().split("\r\n")
        operation  = msgs[0].split(' ', 1)[0]
        msgs[0] = msgs[0].partition(" ")[2]

        ret_val = {}
        data_block = []
        for msg in msgs:
            t = msg.strip().split()
            if operation == "get":
                data_block.append([t[0]])
            elif operation == "set":
                data_block.append([t[0], t[3]])
        ret_val[operation] = data_block
        return ret_val


    @staticmethod
    def parse_first_line(msg):
        msg_parts = msg.split("\r\n")[0].strip().split(" ")
        operation = msg_parts[0]
        key = ""
        val = ""
        data_block = []
        t = None
        if operation == "set":
            bytes = int(msg_parts[4])
            key = msg_parts[1]
            t = (operation,key,bytes)
        elif operation == "get":
            keys = msg_parts[1:]
            # val_arr = msg_parts.partition("get ")[2]
            # for tmp in val_arr:
            #     data_block.append(tmp.strip())
            t = (operation, keys)
        return t
    
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

    @staticmethod
    def parse_get_response(msg):
        """
        VALUE <key> 0 <bytes>\r\n
        <data block>\r\n
        [... more values if multiple keys requested]
        [Note: if a key is not found, there will be no VALUE for it in this list]
        END\r\n
        """

        lines = msg.split("\r\n")
        d = {}
        i = 0
        while i < len(lines):
            if lines[i] == "END":
                break

            if lines[i].startswith("VALUE"):
                parts = lines[i].split(" ")
                key = parts[1]
                value = lines[i+1]
                d[key] = value
                i += 2

        return d

#if __name__ == "__main__":
    #msg = "get aaa 0 0 val\r\nbbb 0 0 val2"
    #msg = "get-servers\r\n"

    #parts = ProtoParser.parse(msg)
    #parts_block = ProtoParser.parse_block(msg)
    #print parts_block
    #print parts_block.iterkeys().next()