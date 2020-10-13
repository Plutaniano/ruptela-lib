class Sim_Card:
    """
    Class for storing sim card data
    ....
    Attributes:
    
    operator: Operator
        Its operator
    
    line: str
        phone number with intl code and area code
    
    ICCID: str
        its ICCID number
    
    name: str
        name of the owner
    """
    all = []

    def __init__(self, operator, line, ICCID, name) -> None:
        Sim_Card.all.append(self)
        self.operator = operator
        self.line = line
        self.ICCID = ICCID
        self.name = name
    
    def __repr__(self) -> str:
        intl_code = self.line[:2]
        area_code = self.line[2:4]
        phone = self.line[4:]
        return f'[SIM] +{intl_code} ({area_code}) {phone[:5]}-{phone[5:]}'