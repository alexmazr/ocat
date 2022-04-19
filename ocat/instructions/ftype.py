from .bytecode import Function

class Send (Function):
    def __init__ (self):
        super ().__init__ ()
        self.opcode = 0