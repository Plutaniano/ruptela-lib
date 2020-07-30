class Data_Packet:
    all = []

    def __init__(self, length, rawbytes):
        self.all.append(self)
        self.length = length
        self.id = rawbytes[0]
        self.param_count = int.from_bytes(rawbytes[1:3], 'little')
        self.data = data_to_parameters(rawbytes[3:])
    
    def __repr__(self):
        return f'[DataPacket][ID:{self.id}][params:{self.param_count}]'
        

class Parameter:
    def __init__(self, param_id, length, value):
        self.id = param_id
        self.length = length
        self.value = value

    def __repr__(self):
        return f'[P][ID:{self.id}][len:{self.length}]'


def data_to_parameters(data):
    parameters = []
    while data:
        param_id = int.from_bytes(data[:2], 'little')
        param_length = int.from_bytes(data[2:3], 'little')
        param_value = int.from_bytes(data[3:3+param_length], 'little')
        parameters.append(Parameter(param_id, param_length, param_value))
        data = data[3+param_length:]
    return parameters