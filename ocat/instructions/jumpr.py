from .bytecode import JumpR

class Jmpzr (JumpR):
    def __init__ (self, reg, pc):
        super ().__init__ (reg, pc)
        self.opcode = 0

class Jmpnzr (JumpR):
    def __init__ (self, reg, pc):
        super ().__init__ (reg, pc)
        self.opcode = 1