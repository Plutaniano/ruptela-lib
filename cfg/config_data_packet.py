from parameter import Parameter

class Config_Data_Packet:
    all = []

    def __init__(self, length, packet_id, param_count, parameters_raw):
        self.all.append(self)
        self.length = length
        self.id = packet_id
        self.param_count = param_count
        self.parameters = []
        while parameters_raw:
            param_id = int.from_bytes(parameters_raw[:2], 'little')
            param_length = int.from_bytes(parameters_raw[2:3], 'little')
            param_value = parameters_raw[3:3+param_length]
            p = Parameter(param_id, param_length, param_value)
            self.parameters.append(p)
            parameters_raw = parameters_raw[2+1+param_length:]
        
    
    def __repr__(self):
        return f'[DataPacket] <ID:{self.id} params:{self.param_count}>'

if __name__ == '__main__':
    from config_file import Config_File
    f = Config_File('config sample.fk4c')