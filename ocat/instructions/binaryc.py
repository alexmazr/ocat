from .bytecode import BinaryC

################################################
# Add Instructions
################################################

class Addcu (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 0
        
class Addci (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 1

class Addcf (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 2

################################################
# Sub Instructions
################################################

class Subcu (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 3

class Subci (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 4

class Subcf (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 5

################################################
# Mul Instructions
################################################

class Mulcu (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 6

class Mulci (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 7

class Mulcf (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 8

################################################
# Div Instructions
################################################

class Divcu (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 9

class Divci (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 10

class Divcf (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 11

################################################
# Exp Instructions
################################################

class Expcu (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 12

class Expci (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 13

class Expcf (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 14

################################################
# Mod Instructions
################################################

class Modcu (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 15

class Modci (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 16

class Modcf (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 17
        
################################################
# Andl Instructions
################################################

class Andcl (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 18

################################################
# Xorl Instructions
################################################

class Xorcl (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 19

################################################
# Orl Instructions
################################################        

class Orcl (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 20
 
################################################
# Eq Instructions
################################################    

class Eqcu (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 21

class Eqci (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 22

class Eqcf (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 23
        
################################################
# Neq Instructions
################################################  

class Neqcu (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 24

class Neqci (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 25

class Neqcf (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 26

################################################
# Gte Instructions
################################################         

class Gtecu (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 27

class Gteci (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 28

class Gtecf (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 29

################################################
# Lte Instructions
################################################     

class Ltecu (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 30

class Lteci (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 31

class Ltecf (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 32

################################################
# Gt Instructions
################################################          

class Gtcu (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 33

class Gtci (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 34

class Gtcf (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 35

################################################
# Lt Instructions
################################################ 

class Ltcu (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 36

class Ltci (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 37

class Ltcf (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 38

################################################
# Andb Instructions
################################################       

class Andcb (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 39

################################################
# Xorb Instructions
################################################       

class Xorcb (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 40
        
################################################
# Orb Instructions
################################################

class Orcb (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 41

################################################
# Shift Instructions
################################################

class Shiftcl (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest)
        self.opcode = 42
        
class Shiftcr (BinaryC):
    def __init__ (self, left, right, dest):
        super ().__init__ (left, right, dest) 
        self.opcode = 43