from .bytecode import FType

class Send (FType):
    def __init__ (self):
        super ().__init__ ()
        self.opcode = 0