from .bytecode import WaitR

class Waitrr (WaitR):
    def __init__ (self, reg):
        super ().__init__ (reg) 
        self.opcode = 0

class Waitra (WaitR):
    def __init__ (self, reg):
        super ().__init__ (reg) 
        self.opcode = 1