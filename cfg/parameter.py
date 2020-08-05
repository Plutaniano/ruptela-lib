class Parameter:
    def __init__(self, param_id, length, value):
        self.id = param_id
        self.length = length
        self.value = value

    def __repr__(self):
        return f'[P] <ID:{self.id} len:{self.length}>'

    def idf(self):
        id = hex(self.id)[2:].zfill(2)
        id = bytes.fromhex(id)
        return id

    def lengthf(self):
        length = hex(self.length)[2:].zfill(4)
        length = bytes([int(length[2:], 16), int(length[:2], 16)])
        return length
   
    def valuef(self):
        value = hex(self.value)[2:].zfill(self.length * 2)
        value = bytes.fromhex(value)[::-1] #[::-1] for Big Endian
        return value
