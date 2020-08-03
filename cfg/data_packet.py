from parameter import Parameter

class Data_Packet:
    all = []

    def __init__(self, length, rawbytes):
        self.all.append(self)
        self.length = length
        self.id = rawbytes[0]
        self.param_count = int.from_bytes(rawbytes[1:3], 'little')
        parameters = []
        while rawbytes:
            param_id = int.from_bytes(rawbytes[:2], 'little')
            param_length = int.from_bytes(rawbytes[2:3], 'little')
            param_value = int.from_bytes(rawbytes[3:3+param_length], 'little')
            p = Parameter(param_id, param_length, param_value)
            parameters.append(p)
            rawbytes = rawbytes[3+param_length:]
        self.data = parameters
    
    def __repr__(self):
        return f'[DataPacket] <ID:{self.id} params:{self.param_count}>'