from .bytecode import BinaryR

################################################
# Add Instructions
################################################

class Addru (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 0
        
class Addri (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 1

class Addrf (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 2

################################################
# Sub Instructions
################################################

class Subru (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 3

class Subri (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 4

class Subrf (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 5

################################################
# Mul Instructions
################################################

class Mulru (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 6

class Mulri (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 7

class Mulrf (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 8

################################################
# Div Instructions
################################################

class Divru (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 9

class Divri (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 10

class Divrf (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 11

################################################
# Exp Instructions
################################################

class Expru (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 12

class Expri (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 13

class Exprf (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 14

################################################
# Mod Instructions
################################################

class Modru (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 15

class Modri (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 16

class Modrf (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 17
        
################################################
# Andl Instructions
################################################

class Andrl (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 18

################################################
# Xorl Instructions
################################################

class Xorrl (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 19

################################################
# Orl Instructions
################################################        

class Orrl (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 20
 
################################################
# Eq Instructions
################################################    

class Eqru (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 21

class Eqri (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 22

class Eqrf (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 23
        
################################################
# Neq Instructions
################################################  

class Neqru (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 24

class Neqri (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 25

class Neqrf (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 26

################################################
# Gte Instructions
################################################         

class Gteru (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 27

class Gteri (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 28

class Gterf (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 29

################################################
# Lte Instructions
################################################     

class Lteru (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 30

class Lteri (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 31

class Lterf (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 32

################################################
# Gt Instructions
################################################          

class Gtru (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 33

class Gtri (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 34

class Gtrf (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 35

################################################
# Lt Instructions
################################################ 

class Ltru (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 36

class Ltri (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 37

class Ltrf (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 38

################################################
# Andb Instructions
################################################       

class Andrb (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 39

################################################
# Xorb Instructions
################################################       

class Xorrb (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 40
        
################################################
# Orb Instructions
################################################

class Orrb (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 41

################################################
# Shift Instructions
################################################

class Shiftrl (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 42
        
class Shiftrr (BinaryR):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest) 
        self.opcode = 43