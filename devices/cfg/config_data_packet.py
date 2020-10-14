from .parameter import Parameter

class Config_Data_Packet:
    """
    Class responsible for storing each data packet in a config file.
    Also provides methods for retrieving information in a convenient format.
    """
    all = []

    def __init__(self, length: int, packet_id: int, param_count: int, parameters_raw: bytes) -> None:
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

    def idf(self) -> bytes:
        return int.to_bytes(self.id, 1, 'little')

    def lengthf(self) -> bytes:
        return int.to_bytes(self.length, 2, 'little')
    
    def param_countf(self) -> bytes:
        return int.to_bytes(self.param_count, 2, 'little')

    def format(self) -> bytes:
        string = b''
        for p in self.parameters:
            string = string + p.idf() + p.lengthf() + p.valuef()
        return self.lengthf() + self.idf() + self.param_countf() + string
    
    def __repr__(self) -> str:
        return f'[Config_Data_Packet] <ID:{self.id} params:{self.param_count}>'

if __name__ == '__main__':
    from . import Config_File
    f = Config_File('config sample.fk4c')