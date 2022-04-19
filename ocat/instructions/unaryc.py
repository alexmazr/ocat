from .bytecode import UnaryC

class Movc (UnaryC):
    def __init__ (self, src, dest):
        super ().__init__ (src, dest) 
        self.opcode = 0

class USubci (UnaryC):
    def __init__ (self, reg, dest):
        super ().__init__ (reg, dest) 
        self.opcode = 1

class USubcf (UnaryC):
    def __init__ (self, reg, dest):
        super ().__init__ (reg, dest) 
        self.opcode = 2
        
class Invc (UnaryC):
    def __init__ (self, reg, dest):
        super ().__init__ (reg, dest) 
        self.opcode = 3
        
class Notc (UnaryC):
    def __init__ (self, reg, dest):
        super ().__init__ (reg, dest)
        self.opcode = 4
         