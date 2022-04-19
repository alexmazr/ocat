from .bytecode import UnaryR

class Movr (UnaryR):
    def __init__ (self, src, dest):
        super ().__init__ (src, dest) 
        self.opcode = 0

class USubri (UnaryR):
    def __init__ (self, reg, dest):
        super ().__init__ (reg, dest) 
        self.opcode = 1

class USubrf (UnaryR):
    def __init__ (self, reg, dest):
        super ().__init__ (reg, dest) 
        self.opcode = 2
        
class Invr (UnaryR):
    def __init__ (self, reg, dest):
        super ().__init__ (reg, dest)
        self.opcode = 3
         
class Notr (UnaryR):
    def __init__ (self, reg, dest):
        super ().__init__ (reg, dest) 
        self.opcode = 4
        