from .bytecode import SingleC

class Waitcr (SingleC):
    def __init__ (self, time):
        super ().__init__ (time) 
        self.opcode = 0

class Waitca (SingleC):
    def __init__ (self, time):
        super ().__init__ (time) 
        self.opcode = 1

class Timeoutcr (SingleC):
    def __init__ (self, time):
        super ().__init__ (time) 
        self.opcode = 2

class Timeoutca (SingleC):
    def __init__ (self, time):
        super ().__init__ (time) 
        self.opcode = 3

class Fetch (SingleC):
    def __init__ (self, id):
        super ().__init__ (id)
        self.opcode = 4

class FetchN (SingleC):
    def __init__ (self, id):
        super ().__init__ (id)
        self.opcode = 5

class Jump (SingleC):
    def __init__ (self, dest):
        super ().__init__ (dest) 
        self.opcode = 6