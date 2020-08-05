class Parameter:
    def __init__(self, param_id, length, value):
        self.id = param_id
        self.length = length
        self.value = value

    def __repr__(self):
        return f'[P] <ID:{self.id} len:{self.length}>'

    def idf(self):
        return int.to_bytes(self.id, 2, 'little')

    def lengthf(self):
        return int.to_bytes(self.length, 1, 'little')
   
    def valuef(self):
        return self.value
