class Parameter:
    def __init__(self, param_id, length, value):
        self.id = param_id
        self.length = length
        self.value = value

    def __repr__(self):
        return f'[P][ID:{self.id}][len:{self.length}]'
