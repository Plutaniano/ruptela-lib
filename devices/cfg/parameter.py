class Parameter:
    """
    Class that stores information about a Config_File's parameter.
    """
    def __init__(self, param_id: int, length: int, value: bytes) -> bytes:
        self.id = param_id
        self.length = length
        self.value = value

    def idf(self) -> bytes:
        return int.to_bytes(self.id, 2, 'little')

    def lengthf(self) -> bytes:
        return int.to_bytes(self.length, 1, 'little')
   
    def valuef(self) -> bytes:
        return self.value

    def __repr__(self) -> str:
        return f'[P] <ID:{self.id}, len:{self.length}>'
