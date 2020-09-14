class Sim_Card:
    all = []

    def __init__(self, operator, line, ICCID, name):
        Sim_Card.all.append(self)
        self.operator = operator
        self.line = line
        self.ICCID = ICCID
        self.name = name
    
    def __repr__(self):
        intl_code = self.line[:2]
        area_code = self.line[2:4]
        phone = self.line[4:]
        return f'[SIM] +{intl_code} ({area_code}) {phone[:5]}-{phone[5:]}'