class Hardware:
    all = []

    def __init__(self, d):
        self.all.append(self)
        self.id = d['id']
        self.name = d['name']
        self.description = d['description']
        self.hw_version = d['hw_version']
        self.soft_id = d['soft_id']
        self.soft_version = d['soft_version']

    @classmethod
    def select_hardware(cls):
        for i, hw in enumerate(cls.all):
            print(f'[ID:{i}] {hw.name}')
        print('\n\n')
        index = int(input('Selecione o ID do hardware a ser utilizado: '))
        return cls.all[index]

    def __repr__(self):
        return f'[HW] {self.name}'