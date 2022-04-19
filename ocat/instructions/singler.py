from .bytecode import SingleR

class Waitrr (SingleR):
    def __init__ (self, reg):
        super ().__init__ (reg)
        self.opcode = 0

class Waitra (SingleR):
    def __init__ (self, reg):
        super ().__init__ (reg)
        self.opcode = 1

class Timeoutrr (SingleR):
    def __init__ (self, reg):
        super ().__init__ (reg)
        self.opcode = 2

class Timeoutra (SingleR):
    def __init__ (self, reg):
        super ().__init__ (reg)
        self.opcode = 3

