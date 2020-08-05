from parameter import Parameter

class Config_Data_Packet:
    all = []

    def __init__(self, length, rawbytes):
        self.all.append(self)
        self.length = length
        self.id = int.from_bytes(rawbytes[:1], 'little')
        self.param_count = int.from_bytes(rawbytes[1:3], 'little')
        rawbytes = rawbytes[3:]
        parameters = []
        while rawbytes:
            param_id = int.from_bytes(rawbytes[:2], 'little')
            param_length = int.from_bytes(rawbytes[2:3], 'little')
            param_value = int.from_bytes(rawbytes[3:3+param_length], 'little')
            p = Parameter(param_id, param_length, param_value)
            parameters.append(p)
            rawbytes = rawbytes[3+param_length:]
        self.data = parameters

    def lengthf(self):
        length = hex(self.length)[2:].zfill(4)
        length = bytes([int(length[2:], 16), int(length[:2], 16)])
        return length

    def idf(self):
        id = hex(self.id)[2:].zfill(2)
        id = bytes.fromhex(id)
        return id
    
    def param_countf(self):
        param_count = hex(self.param_count)[2:].zfill(4)
        param_count = bytes([int(param_count[2:], 16), int(param_count[:2], 16)])
        return param_count

    def format(self):
        string = b''
        for p in self.data:
            string = string + p.idf() + p.lengthf() + p.valuef()
        return self.lengthf() + self.idf() + self.param_countf() + string
    
    def __repr__(self):
        return f'[Config_Data_Packet] <ID:{self.id} params:{self.param_count}>'

if __name__ == '__main__':
    from config_file import Config_File
    f = Config_File('config sample.fk4c')